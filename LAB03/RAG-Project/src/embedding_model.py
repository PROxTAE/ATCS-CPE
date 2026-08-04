


"""
wrap sentence-transformers for easier usage
model that converts text into embeddings, where semantically similar texts will have embeddings that are 
"close" to each other in a high-dimensional space

"""

from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name):
        print(f"[embedding_model] Loading model: {model_name} ...")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        print("[embedding_model] Model loaded successfully.")

    def encode(self, texts):
        """
        Convert a list of texts into a numpy array of embeddings
        The shape of the returned array is (texts number, embeddings dimension)
        """
        # If using an E5 model, prepend 'passage: ' to all documents/passages
        if "e5" in self.model_name.lower():
            processed_texts = []
            for text in texts:
                if not text.startswith("passage: "):
                    processed_texts.append(f"passage: {text}")
                else:
                    processed_texts.append(text)
            texts = processed_texts

        return self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True,  # normalize ไว้ล่วงหน้า เพื่อให้ค้นด้วย cosine similarity ง่ายขึ้น
        )

    def encode_query(self, query_text):
        """Convert a single query into a vector"""
        if "e5" in self.model_name.lower() and not query_text.startswith("query: "):
            query_text = f"query: {query_text}"
        return self.model.encode([query_text], normalize_embeddings=True)[0]
