import csv
import torch
from transformers import BertTokenizer, BertModel

# Load the tokenizer and model
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")

filename = "semantic_tag_1500.tsv"
titles = []

with open(filename, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file, delimiter="\t")
    for row in reader:
        titles.append(row["title"])

batch_size = 10
title_to_vector = {}

for i in range(0, len(titles), batch_size):
    batch_titles = titles[i : i + batch_size]
    encoded_input = tokenizer(
        batch_titles, return_tensors="pt", padding=True, truncation=True, max_length=128
    )
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

    for title, embedding in zip(batch_titles, mean_embeddings):
        title_to_vector[title] = embedding

# Save the dictionary
torch.save(title_to_vector, "title_to_vector_1500.pt")

print(
    f"Saved the title to vector mappings for {len(titles)} titles in 'title_to_vector_1500.pt'."
)
