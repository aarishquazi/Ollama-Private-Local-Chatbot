from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

class VectorDatabase:
    def __init__(self):
        self.db_path = "data/vector_db"
        Path(self.db_path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        try:
            self.collection = self.client.get_collection("documents")
        except:
            self.collection = self.client.create_collection("documents")

    def add_documents(self, documents):
        texts = [d['text'] for d in documents]
        embs = self.embedding_model.encode(texts).tolist()
        self.collection.add(
            ids=[d['id'] for d in documents],
            documents=texts,
            embeddings=embs,
            metadatas=[{"source": d['source'], "chunk": d['chunk']} for d in documents]
        )

    def search(self, query: str, limit: int = 5):
        emb = self.embedding_model.encode([query]).tolist()
        results = self.collection.query(query_embeddings=emb, n_results=limit)
        return [{"text": results['documents'][0][i], "source": results['metadatas'][0][i]['source']} for i in range(len(results['ids'][0]))]

    def count_documents(self):
        return self.collection.count()