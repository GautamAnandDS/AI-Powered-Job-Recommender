# src/embeddings_store.py
import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

EMB_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./data/vectorstore.faiss")
META_PATH = VECTORSTORE_PATH + ".meta.pkl"

class VectorStore:
    def __init__(self, model_name=EMB_MODEL):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.metadatas = []

    def _job_to_text(self, j: dict) -> str:
        # Concise, relevant text only
        return "\n".join(filter(None, [
            j.get("title", ""),
            j.get("organization", ""),
            j.get("employment_type", ""),
            j.get("locations_derived", ""),
            j.get("linkedin_org_description", ""),
            j.get("seniority", "")
        ]))

    def build_from_jobs(self, jobs: list[dict]):
        docs = []
        self.metadatas = []
        for j in jobs:
            docs.append(self._job_to_text(j))
            self.metadatas.append({
                "id": j.get("id"),
                "title": j.get("title"),
                "organization": j.get("organization"),
                "url": j.get("url"),
                "employment_type": j.get("employment_type"),
                "locations_derived": j.get("locations_derived"),
                "seniority": j.get("seniority"),
                "raw": j
            })

        embs = self.model.encode(docs, show_progress_bar=False, convert_to_numpy=True, normalize_embeddings=True)
        dim = embs.shape[1]
        index = faiss.IndexFlatIP(dim)   # cosine via normalized vectors
        index.add(embs)
        self.index = index

        faiss.write_index(index, VECTORSTORE_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadatas, f)

    def load(self):
        if not os.path.exists(VECTORSTORE_PATH):
            raise FileNotFoundError("Vectorstore not found")
        self.index = faiss.read_index(VECTORSTORE_PATH)
        with open(META_PATH, "rb") as f:
            self.metadatas = pickle.load(f)

    def query(self, text: str, top_k: int = 5):
        if self.index is None:
            self.load()
        q = self.model.encode([text], convert_to_numpy=True, normalize_embeddings=True)
        D, I = self.index.search(q, top_k)
        return [self.metadatas[i] for i in I[0] if i < len(self.metadatas)]
