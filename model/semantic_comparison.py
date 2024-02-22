import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import logging
from datetime import datetime

log_dir = "log"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Set logger
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_filename = f"similarity_{current_time}.log"
logging.basicConfig(
    filename=os.path.join(log_dir, log_filename),
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")


# Using Mean Pooling
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = input_mask_expanded.sum(1)
    sum_mask = torch.clamp(sum_mask, min=1e-9)
    mean_embeddings = sum_embeddings / sum_mask
    return mean_embeddings


text = "幫找一些便宜美食的文章"
encoded_input = tokenizer(
    text, return_tensors="pt", padding=True, truncation=True, max_length=256
)

# Generate embeddings for the input text
with torch.no_grad():
    model_output = model(**encoded_input)
    sentence_embedding = mean_pooling(
        model_output, encoded_input["attention_mask"]
    ).numpy()

# Load the title to vector mappings
title_to_vector = torch.load("title_to_vector_1500.pt")
titles = list(title_to_vector.keys())
embeddings = torch.stack(list(title_to_vector.values())).squeeze(1).numpy()

# Calculate cosine similarity between the input text and each title
similarities = cosine_similarity(sentence_embedding, embeddings)[0]

# Display similarity score
for title, similarity in zip(titles, similarities):
    print(f"Similarity for title '{title}': {similarity}")
    logging.info(f"Similarity for title '{title}': {similarity}")

top_10_idx = similarities.argsort()[-10:][::-1]
top_10_titles = []

logging.info("Top 10 most similar titles:")
for rank, idx in enumerate(top_10_idx, start=1):
    top_title = titles[idx]
    top_similarity = similarities[idx]
    print(f"Rank {rank}: '{top_title}', Similarity score: {top_similarity}")
    logging.info(f"Rank {rank}: '{top_title}', Similarity score: {top_similarity}")
    top_10_titles.append(top_title)

print("Logger saved.")
