"""
LAB 05: Encode English user queries into embedding vectors.

Run: python labs/lab05_query_embedding.py
"""

import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import config
from src.embedding_model import EmbeddingModel


def main():
    print("=== Lab 05: English Query Embedding ===")
    test_query = "What is the difference between single-coil and humbucker pickups?"
    print(f"Test Query: '{test_query}'")

    embedding_model = EmbeddingModel()
    query_vector = embedding_model.encode_query(test_query)

    print(f"Embedding Model: {config.EMBEDDING_MODEL_NAME}")
    print(f"Vector Shape   : {query_vector.shape}")
    print(f"First 5 Values : {query_vector[:5]}")
    print(f"L2 Norm        : {float((query_vector**2).sum()**0.5):.4f}")


if __name__ == "__main__":
    main()
