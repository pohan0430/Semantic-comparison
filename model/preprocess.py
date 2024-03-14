import csv
import torch
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import jieba
import re

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the stsb model
model = SentenceTransformer("distiluse-base-multilingual-cased-v2").to(device)
# model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2").to(device)
# model = SentenceTransformer("all-mpnet-base-v2").to(device)

filename = "semantic_tag_2023_7_1-2024_2_20.tsv"
news_data = []


# Text preprocess
def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(jieba.cut(text))
    return text


with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in tqdm(reader, desc="Reading file"):
        title_original = row["title"]
        title_clean = preprocess_text(row["title"])
        content_clean = preprocess_text(row["content_clean"])
        news_data.append(
            (
                row["news_id"],
                title_original,
                title_clean,
                content_clean,
                row["cat_lv1"],
                row["cat_lv2"],
                row["tags"],
                row["url"],
                row["event_date"],
            )
        )

batch_size = 100
news_info_to_vector = {}

for i in tqdm(range(0, len(news_data), batch_size), desc="Processing news data"):
    batch = news_data[i : i + batch_size]
    batch_titles_cleaned = [
        title_clean for _, _, title_clean, _, _, _, _, _, _ in batch
    ]
    embeddings = model.encode(batch_titles_cleaned, convert_to_tensor=True)

    for item, embedding in zip(batch, embeddings):
        news_id = item[0]
        info_key = {
            "news_id": news_id,
            "title": item[1],
            "content_clean": item[2],
            "cat_lv1": item[3],
            "cat_lv2": item[4],
            "tags": item[5],
            "url": item[6],
            "event_date": item[7],
            "vector": embedding.cpu().numpy(),
        }
        news_info_to_vector[news_id] = info_key


# Save the dictionary
dict_name = "DistilBERT.pt"
torch.save(news_info_to_vector, dict_name)

print(
    f"Saved the news information and vector mappings for {len(news_data)} items in pt file."
)
