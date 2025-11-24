from sentence_transformers import SentenceTransformer
import torch
import numpy as np


class Vectorizer:

    def __init__(self):
        MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

        self.device = torch.device("cpu")

        try:
            self.model = SentenceTransformer(MODEL_NAME, device=self.device)
        except Exception as e:
            print(f"Ошибка загрузки модели: {e}. Проверьте имя модели.")
            exit()

        self.model.to(self.device)
        self.model.eval()

    def add_vector_to_articles(self, articles):

        for article in articles:
            article.set_vector(self.encode_text(article.origin_text))

    def encode_text(self, text):

        embeddings = self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.astype(np.float32)