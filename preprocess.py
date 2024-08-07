import requests
from zipfile import ZipFile
import pandas as pd
import numpy as np
from io import BytesIO
from argparse import ArgumentParser
import json
import re
import os
import tqdm
import jieba
from backend.model.semantic_comparison import model
from tqdm import tqdm


def parse_args():
    parser = ArgumentParser()
    parser.add_argument(
        "--table_name", type=str, help="table name in dora", default="exp_semantic_tag"
    )
    parser.add_argument(
        "--export_date", type=str, help="export date in dora", default=None
    )
    args = parser.parse_args()
    return args


def download_csv(args) -> pd.DataFrame:
    table_name = args.table_name
    export_date = args.export_date

    url = f"https://dora.ettoday.net/export/eds/{table_name}.zip?version={export_date}_000000&format=tsv"

    response = requests.get(url, stream=True)

    if response.status_code == 200:
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        block_size = 1024

        with tqdm(
            total=total_size_in_bytes, unit="iB", unit_scale=True, desc="Downloading..."
        ) as progress_bar:
            with BytesIO() as memory_file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    memory_file.write(data)

                memory_file.seek(0)
                with ZipFile(memory_file) as zip_file:
                    tsv_content = zip_file.read(zip_file.namelist()[0])

        df = pd.read_csv(BytesIO(tsv_content), sep="\t", encoding="utf-8")

        return df
    else:
        print(
            f"Failed to download the file. table name: {table_name}, export date : {export_date}, status code: {response.status_code}"
        )
        raise ValueError


# Text preprocess
def process_text(text: str) -> str:
    if pd.isna(text):
        return ""
    text = re.sub(r"[^\w\s,]", "", text)
    segments = text.split(",")
    processed_segments = [" ".join(jieba.cut(segment)) for segment in segments]
    return " ".join(processed_segments)


def embedding(df: pd.DataFrame, batch_size: int = 100) -> pd.DataFrame:
    print("embedding...")

    df["vector"] = np.nan
    title_clean = df["title"].apply(process_text)
    keywords_clean = df["keywords"].apply(process_text)
    for i in tqdm(range(0, df.shape[0], batch_size), desc="Processing news data"):
        combined_texts = [
            t + " " + k
            for t, k in zip(
                title_clean.iloc[i : i + batch_size],
                keywords_clean.iloc[i : i + batch_size],
            )
        ]
        embeddings = model.encode(combined_texts, convert_to_tensor=False)
        df.loc[i : i + batch_size - 1, "vector"] = [
            json.dumps(embedding.tolist()) for embedding in embeddings
        ]
    return df


if __name__ == "__main__":
    args = parse_args()

    df = download_csv(args)

    df = embedding(df)

    os.makedirs("data", exist_ok=True)

    df.to_csv("./data/news_embedding.csv", index=False)
