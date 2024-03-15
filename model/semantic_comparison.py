import os
import torch
import jieba
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np
import logging
from datetime import datetime


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = SentenceTransformer("distiluse-base-multilingual-cased-v2").to(device)
# model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2").to(device)


def set_logger():
    """
    Initialize logging configuration.
    Input: None
    Output: None
    """
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


def preprocess_text(text: str) -> str:
    """
    Remove non-word characters and use jieba for word segmentation.
    Input: str
    Output: str
    """
    text = re.sub(r"[^\w\s]", "", text)
    text = " ".join(jieba.cut(text))
    return text


def get_embedding(input_text: str) -> np.ndarray:
    """
    Generate embedding vector for the input text.
    Input: str
    Output: np.ndarray
    """
    input_text = preprocess_text(input_text)
    sentence_embedding = model.encode(input_text, convert_to_tensor=False)
    return sentence_embedding


def find_similar_titles_urls(input_text: str, top_n_rank: int = 100) -> list:
    """
    Find the titles most similar to the input text and return the news_id ranking list.
    Input: input_text (str), top_n_rank (int)
    Output: list
    """
    set_logger()
    sentence_embedding = get_embedding(input_text)
    abs_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(abs_path)
    file_path = os.path.join(current_dir, "DistilBERT.pt")
    info_to_vector = torch.load(file_path, map_location=device)

    all_news_embeddings = torch.stack(
        [
            torch.tensor(info["vector"], dtype=torch.float)
            for _, info in info_to_vector.items()
        ]
    )

    similarities = util.cos_sim(sentence_embedding, all_news_embeddings).squeeze(0)

    top_indices = similarities.argsort(descending=True)[:top_n_rank]
    top_news_ids = [list(info_to_vector.keys())[idx] for idx in top_indices]

    for rank, idx in enumerate(top_indices, start=1):
        news_id = list(info_to_vector.keys())[idx]
        info = info_to_vector[news_id]
        top_similarity = similarities[idx].item()
        logging.info(
            f"Rank: {rank} - News ID: {news_id}, Title: {info['title']}, Similarity score: {top_similarity}"
        )

    return top_news_ids


if __name__ == '__main__':
    top_news_ids = find_similar_titles_urls("提供購買房子建議", top_n_rank=50)
