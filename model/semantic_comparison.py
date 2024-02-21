import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity

tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
model = BertModel.from_pretrained("bert-base-chinese")
text = "幫找一些便宜美食的文章"
encoded_input = tokenizer(text, return_tensors="pt")

# Generate embeddings for the input text
with torch.no_grad():
    outputs = model(**encoded_input)
sentence_embedding = outputs.last_hidden_state[:, 0, :].numpy()

# Load the title to vector mappings
title_to_vector = torch.load("title_to_vector_1500.pt")
titles = list(title_to_vector.keys())
embeddings = torch.stack(list(title_to_vector.values())).squeeze(1).numpy()

# Calculate cosine similarity between the input text and each title
similarities = cosine_similarity(sentence_embedding, embeddings)

# Display similarity scores
for title, similarity in zip(titles, similarities[0]):
    print(f"Similarity for title '{title}': {similarity}")


# Find the most similar title
most_similar_idx = similarities.argmax()
most_similar_title = titles[most_similar_idx]
most_similar_score = similarities[0, most_similar_idx]
print(
    f"Most similar title: '{most_similar_title}', Similarity score: {most_similar_score}"
)
