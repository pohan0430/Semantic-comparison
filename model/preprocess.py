import csv
import torch
from transformers import BertTokenizer, BertModel
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese").to(device)

filename = "semantic_tag_2023_7_1-2024_2_20.tsv"
news_data = []

with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in tqdm(reader, desc="Reading file"):
        news_data.append(
            (
                row["news_id"],
                row["title"],
                row["content_clean"],
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
    batch_titles = [title for _, title, _, _, _, _, _, _ in batch]
    encoded_input = tokenizer(
        batch_titles, return_tensors="pt", padding=True, truncation=True, max_length=128
    ).to(device)
    attention_mask = encoded_input["attention_mask"]

    with torch.no_grad():
        outputs = model(**encoded_input)

    # Mean Pooling
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(outputs.last_hidden_state.size()).float()
    )
    sum_embeddings = torch.sum(outputs.last_hidden_state * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    mean_embeddings = sum_embeddings / sum_mask

    for item, embedding in zip(batch, mean_embeddings):
        info_key = {
            "news_id": item[0],
            "title": item[1],
            "cat_lv1": item[3],
            "cat_lv2": item[4],
            "tags": item[5],
            "url": item[6],
            "event_date": item[7],
        }
        news_info_to_vector[f"{item[0]} | {item[1]}"] = {
            "info": info_key,
            "vector": embedding.cpu().numpy(),
        }

# Save the dictionary
torch.save(news_info_to_vector, "news_info_to_vector_2023_7_1-2024_2_20.pt")

print(
    f"Saved the news information and vector mappings for {len(news_data)} items in 'news_info_to_vector.pt'."
)
