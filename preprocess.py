import requests
from zipfile import ZipFile
import pandas as pd
import numpy as np
from io import BytesIO
from argparse import ArgumentParser
import json
import re
import os
import jieba
from model.semantic_comparison import model
from tqdm import tqdm

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--table_name", type=str, help="table name in dora", default='exp_semantic_tag')
    parser.add_argument("--export_date", type=str, help="export date in dora", default=None)
    args = parser.parse_args()
    return args


def download_csv(args) -> pd.DataFrame:
    print('downloading...')
    table_name = args.table_name
    export_date = args.export_date

    url = f"https://dora.ettoday.net/export/eds/{table_name}.zip?version={export_date}_000000&format=tsv"

    response = requests.get(url)

    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip_file:
            tsv_content = zip_file.read(zip_file.namelist()[0])

        df = pd.read_csv(BytesIO(tsv_content), sep='\t', encoding='utf-8')

        return df
    else:
        print(f"Failed to download the file. table name: {table_name}, export date : {export_date}, status code: {response.status_code}")
        raise ValueError


# Text preprocess
def process_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(jieba.cut(text))
    return text


def embedding(df: pd.DataFrame, batch_size: int=100) -> pd.DataFrame:
    print('embedding...')

    df['vector'] = np.nan
    title_clean = df['title'].apply(process_text)
    batch_size = 10
    for i in tqdm(range(0, df.shape[0], batch_size), desc="Processing news data"):
        embeddings = model.encode(title_clean.loc[i:i + batch_size - 1].tolist())
        df.loc[i:i + batch_size - 1, 'vector'] = [json.dumps(x) for x in embeddings.tolist()]
    return df


if __name__ == '__main__':
    args = parse_args()

    df = download_csv(args)

    df = embedding(df)

    os.makedirs('data', exist_ok=True)

    df.to_csv('./data/news_embedding.csv', index=False)
