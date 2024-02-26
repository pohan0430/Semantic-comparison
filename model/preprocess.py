import csv
import torch
from transformers import BertTokenizer, BertModel
from tqdm import tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese").to(device)

filename = "semantic_tag_2023_7_1-2024_2_20.tsv"
titles_and_urls = []

with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in tqdm(reader, desc="Reading file"):
        titles_and_urls.append((row["title"], row["url"]))

batch_size = 100
title_url_to_vector = {}

for i in tqdm(
    range(0, len(titles_and_urls), batch_size), desc="Processing titles and URLs"
):
    batch = titles_and_urls[i : i + batch_size]
    batch_titles = [title for title, url in batch]
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

    for (title, url), embedding in zip(batch, mean_embeddings):
        title_url_to_vector[f"{title} | {url}"] = embedding.cpu().numpy()

# Save the dictionary
torch.save(title_url_to_vector, "title_url_to_vector_2023_7_1-2024_2_20.pt")

print(
    f"Saved the title and URL to vector mappings for {len(titles_and_urls)} items in 'title_url_to_vector.pt'."
)
