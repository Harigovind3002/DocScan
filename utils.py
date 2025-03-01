import openai
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from openai import OpenAI

# Initialize the OpenAI client
from sentence_transformers import SentenceTransformer

# Load a pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    """
    Get embedding for a given text using a local model.
    """
    try:
        embedding = model.encode(text)
        return embedding
    except Exception as e:
        print(f"Embedding Error: {e}")
        return None
    
def calculate_similarity(text1, text2):
    """
    Calculate cosine similarity between two texts using local embeddings.
    """
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)
    if embedding1 is None or embedding2 is None:
        return 0.0  # Return 0 if embeddings are not generated
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    return similarity