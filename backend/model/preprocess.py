import csv
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import jieba
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the stsb model
model = SentenceTransformer("distiluse-base-multilingual-cased-v2").to(device)

filename = "semantic_tag.tsv"
news_data = []


# Text preprocess
def preprocess_text(text: str) -> str:
    text = re.sub(r"[^\w\s,]", "", text)
    segments = text.split(",")
    processed_segments = [" ".join(jieba.cut(segment)) for segment in segments]
    return " ".join(processed_segments)


with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in tqdm(reader, desc="Reading file"):
        title_original = row["title"]
        title_clean = preprocess_text(row["title"])
        content_clean = preprocess_text(row["content"])
        keywords_clean = preprocess_text(row["keywords"])
        news_data.append(
            (
                row["news_id"],
                title_original,
                title_clean,
                content_clean,
                row["cat_lv1"],
                row["cat_lv2"],
                keywords_clean,
                row["url"],
                row["date"],
            )
        )

batch_size = 100
news_info_to_vector = {}

for i in tqdm(range(0, len(news_data), batch_size), desc="Processing news data"):
    batch = news_data[i : i + batch_size]
    batch_titles_cleaned = [
        title_clean for _, _, title_clean, _, _, _, _, _, _ in batch
    ]
    batch_keywords_cleaned = [
        keywords_clean for _, _, _, _, _, _, keywords_clean, _, _ in batch
    ]

    title_embeddings = model.encode(
        batch_titles_cleaned, convert_to_tensor=True, device=device
    )
    keywords_embeddings = model.encode(
        batch_keywords_cleaned, convert_to_tensor=True, device=device
    )
    embeddings = (title_embeddings + keywords_embeddings) / 2

    for item, embedding in zip(batch, embeddings):
        news_id = item[0]
        info_key = {
            "news_id": news_id,
            "title": item[1],
            "content_clean": item[3],
            "cat_lv1": item[4],
            "cat_lv2": item[5],
            "tags": item[6],
            "url": item[7],
            "event_date": item[8],
            "vector": embedding.cpu().numpy(),
        }
        news_info_to_vector[news_id] = info_key

# Save the dictionary
dict_name = "DistilBERT.pt"
torch.save(news_info_to_vector, dict_name)

print(
    f"Saved the news information and vector mappings for {len(news_data)} items in pt file."
)
