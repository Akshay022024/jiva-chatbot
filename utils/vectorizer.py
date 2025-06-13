import os
from typing import List, Tuple
import pickle
from sklearn.neighbors import NearestNeighbors
import numpy as np

# Import sentence-transformers with torch warning suppression
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

try:
    # Suppress torch warnings
    os.environ["TOKENIZERS_PARALLELISM"] = "false"
    from sentence_transformers import SentenceTransformer
except ImportError as e:
    raise ImportError(f"sentence-transformers is required: {e}")

class TextVectorizer:
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            raise RuntimeError(f"Failed to load sentence transformer model: {e}")
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

    def create_vector_store(self, chunks: List[str]) -> Tuple[NearestNeighbors, np.ndarray]:
        """Create sklearn NearestNeighbors vector store from text chunks."""
        # Create embeddings
        embeddings = self.model.encode(chunks)
        embeddings = np.array(embeddings).astype('float32')
        
        # Initialize NearestNeighbors index
        index = NearestNeighbors(n_neighbors=min(3, len(chunks)), metric='cosine', algorithm='auto')
        index.fit(embeddings)
        
        return index, embeddings

    def save_vector_store(self, file_path: str, index: NearestNeighbors, chunks: List[str], embeddings: np.ndarray):
        """Save the vector store to disk."""
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            pickle.dump({
                'index': index,
                'chunks': chunks,
                'embeddings': embeddings
            }, f)

    def load_vector_store(self, file_path: str) -> Tuple[NearestNeighbors, List[str], np.ndarray]:
        """Load the vector store from disk."""
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        return data['index'], data['chunks'], data['embeddings']

    def search(self, query: str, index: NearestNeighbors, chunks: List[str], k: int = 3) -> List[Tuple[str, float]]:
        """Search for relevant chunks given a query."""
        query_vector = self.model.encode([query])
        query_vector = np.array(query_vector).astype('float32').reshape(1, -1)
        
        k = min(k, len(chunks))  # Ensure k doesn't exceed number of chunks
        distances, indices = index.kneighbors(query_vector, n_neighbors=k)
        
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            results.append((chunks[idx], float(distance)))
        
        return results

if __name__ == "__main__":
    INPUT_FILE = os.path.join("data", "website_data.txt")
    OUTPUT_FILE = os.path.join("data", "vector_store.pkl")
    
    vectorizer = TextVectorizer()
    
    # Read input text
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Create chunks and vector store
    chunks = vectorizer.get_text_chunks(text)
    index, embeddings = vectorizer.create_vector_store(chunks)
    vectorizer.save_vector_store(OUTPUT_FILE, index, chunks, embeddings)
    
    print(f"Vector store created and saved to {OUTPUT_FILE}")
