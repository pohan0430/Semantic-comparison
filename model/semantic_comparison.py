import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import logging
from datetime import datetime


def set_logger():
    log_dir = "log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = f"similarity_{current_time}.log"
    logging.basicConfig(
        filename=os.path.join(log_dir, log_filename),
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output.last_hidden_state
    input_mask_expanded = (
        attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    )
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = input_mask_expanded.sum(1)
    sum_mask = torch.clamp(sum_mask, min=1e-9)
    mean_embeddings = sum_embeddings / sum_mask
    return mean_embeddings.numpy()


def find_similar_titles_urls(input_text):
    set_logger()
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    model = BertModel.from_pretrained("bert-base-chinese")

    encoded_input = tokenizer(
        input_text, return_tensors="pt", padding=True, truncation=True, max_length=256
    )
    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_embedding = mean_pooling(
            model_output, encoded_input["attention_mask"]
        ).squeeze(0)

    base_dir = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(
        base_dir, "model", "title_url_to_vector_2023_7_1-2024_2_20.pt"
    )
    title_url_to_vector = torch.load(file_path)
    titles_urls = list(title_url_to_vector.keys())
    tensor_list = [
        torch.tensor(value, dtype=torch.float) for value in title_url_to_vector.values()
    ]
    embeddings = torch.stack(tensor_list).numpy()

    similarities = cosine_similarity([sentence_embedding], embeddings)[0]
    top_100_idx = similarities.argsort()[-100:][::-1]
    top_100_titles_urls = []

    logging.info("Top 100 most similar titles and URLs:")
    for rank, idx in enumerate(top_100_idx, start=1):
        top_title_url = titles_urls[idx]
        top_similarity = float(similarities[idx])
        logging.info(
            f"Rank {rank}: '{top_title_url}', Similarity score: {top_similarity}"
        )
        top_100_titles_urls.append((top_title_url, top_similarity))

    return top_100_titles_urls
