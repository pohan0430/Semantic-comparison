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

# Generate vector for each title
title_to_vector = {}
for title in titles:
    encoded_input = tokenizer(title, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**encoded_input)
    title_embedding = outputs.last_hidden_state[:, 0, :]
    title_to_vector[title] = title_embedding
print(title_to_vector)
# Save the dictionary
torch.save(title_to_vector, "title_to_vector_1500.pt")

print(
    f"Saved the title to vector mappings for {len(titles)} titles in 'title_to_vector.pt'."
)
