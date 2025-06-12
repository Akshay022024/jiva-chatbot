import os
from typing import List, Tuple
import pickle
from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer
import numpy as np

class TextVectorizer:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.chunk_size = 400  # approximate tokens per chunk
        self.overlap = 50  # overlap between chunks

    def get_text_chunks(self, text: str) -> List[str]:
        """Split text into overlapping chunks."""
        words = text.split()
        chunks = []
        
        i = 0
        while i < len(words):
            chunk = ' '.join(words[i:i + self.chunk_size])
            chunks.append(chunk)
            i += (self.chunk_size - self.overlap)
            
        return chunks

    def create_vector_store(self, chunks: List[str]) -> Tuple[faiss.Index, int]:
        """Create FAISS vector store from text chunks."""
        # Create embeddings
        embeddings = self.model.encode(chunks)
        
        # Initialize FAISS index
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        
        # Add vectors to index
        index.add(np.array(embeddings).astype('float32'))
        
        return index, dimension

    def save_vector_store(self, file_path: str, index: faiss.Index, chunks: List[str], dimension: int):
        """Save the vector store to disk."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump({
                'index': index,
                'chunks': chunks,
                'dimension': dimension
            }, f)

    def load_vector_store(self, file_path: str) -> Tuple[faiss.Index, List[str], int]:
        """Load the vector store from disk."""
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data['index'], data['chunks'], data['dimension']

    def search(self, query: str, index: faiss.Index, chunks: List[str], k: int = 3) -> List[Tuple[str, float]]:
        """Search for relevant chunks given a query."""
        query_vector = self.model.encode([query])
        distances, indices = index.search(np.array(query_vector).astype('float32'), k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            results.append((chunks[idx], float(distance)))
        
        return results

if __name__ == "__main__":
    INPUT_FILE = os.path.join("data", "website_data.txt")
    OUTPUT_FILE = os.path.join("data", "vector_store.pkl")
    
    vectorizer = TextVectorizer()
    vectorizer.create_vector_store(INPUT_FILE, OUTPUT_FILE)
    print(f"Vector store created and saved to {OUTPUT_FILE}")
