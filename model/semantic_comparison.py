import os
import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
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
    return mean_embeddings.detach()


def find_similar_titles_urls(input_text, top_n_rank=100):
    set_logger()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
    model = BertModel.from_pretrained("bert-base-chinese").to(device)

    encoded_input = tokenizer(
        input_text, return_tensors="pt", padding=True, truncation=True, max_length=256
    ).to(device)
    with torch.no_grad():
        model_output = model(**encoded_input)
        sentence_embedding = (
            mean_pooling(model_output, encoded_input["attention_mask"])
            .squeeze(0)
            .cpu()
            .numpy()
        )

    abs_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(abs_path)
    file_path = os.path.join(current_dir, "info_to_vector_2023_7_1-2024_2_20.pt")
    info_to_vector = torch.load(file_path, map_location=torch.device("cpu"))

    similarities = cosine_similarity(
        [sentence_embedding],
        np.array([info["vector"] for info in info_to_vector.values()]),
    )[0]
    for idx, (_, info) in enumerate(info_to_vector.items()):
        logging.info(f"Title: {info['info']['title']}, Similarity: {similarities[idx]}")

    top_indices = np.argsort(similarities)[-top_n_rank:][::-1]
    top_results = []

    logging.info(f"Top {top_n_rank} most similar titles and URLs:")
    for rank, idx in enumerate(top_indices, start=1):
        item = list(info_to_vector.items())[idx]
        top_info = item[1]["info"]
        top_similarity = float(similarities[idx])
        top_info["similarity_score"] = top_similarity
        logging.info(
            f"Rank: {rank}- Title: {top_info['title']}, Similarity score: {top_similarity}"
        )
        top_results.append(top_info)

    return top_results


find_similar_titles_urls("找便宜美食", top_n_rank=100)
