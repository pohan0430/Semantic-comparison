import os
import torch
import jieba
import re
from sentence_transformers import SentenceTransformer, util
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


def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(jieba.cut(text))
    return text


def get_embedding(input_text):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SentenceTransformer("distiluse-base-multilingual-cased-v2").to(device)
    # model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2").to(device)
    # model = SentenceTransformer("all-mpnet-base-v2").to(device)
    input_text = preprocess_text(input_text)
    sentence_embedding = model.encode(input_text, convert_to_tensor=False)
    return sentence_embedding


def find_similar_titles_urls(input_text, top_n_rank=100):
    set_logger()
    sentence_embedding = get_embedding(input_text)
    abs_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(abs_path)
    file_path = os.path.join(current_dir, "DistilBERT.pt")
    # file_path = os.path.join(current_dir, "mpnet.pt")
    info_to_vector = torch.load(file_path, map_location=torch.device("cpu"))

    all_news_embeddings = torch.stack(
        [
            torch.tensor(info["vector"], dtype=torch.float)
            for _, info in info_to_vector.items()
        ]
    )

    similarities = util.cos_sim(sentence_embedding, all_news_embeddings).squeeze(0)

    for idx, (news_id, info) in enumerate(info_to_vector.items()):
        similarity_score = similarities[idx].item()
        logging.info(
            f"News ID: {news_id}, Title: {info['title']}, Similarity: {similarity_score}"
        )

    top_indices = similarities.argsort(descending=True)[:top_n_rank]
    top_news_ids = [list(info_to_vector.keys())[idx] for idx in top_indices]

    logging.info(f"Top {top_n_rank} most similar titles:")
    for rank, idx in enumerate(top_indices, start=1):
        news_id = list(info_to_vector.keys())[idx]
        info = info_to_vector[news_id]
        top_similarity = similarities[idx].item()
        logging.info(
            f"Rank: {rank} - News ID: {news_id}, Title: {info['title']}, Similarity score: {top_similarity}"
        )

    return top_news_ids


top_news_ids = find_similar_titles_urls("提供購買房子建議", top_n_rank=50)
