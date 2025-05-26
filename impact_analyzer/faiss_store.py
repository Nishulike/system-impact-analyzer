from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GooglePalmEmbeddings
import os

class FaissStore:
    def __init__(self, index_path="faiss_index_dir"):
        self.index_path = index_path
        self.embeddings = GooglePalmEmbeddings()
        self.faiss_index = None
        
        # Load existing FAISS index if present, else raise error or create empty index
        if os.path.exists(self.index_path):
            self.faiss_index = FAISS.load_local(self.index_path, self.embeddings)
        else:
            raise FileNotFoundError(f"FAISS index directory '{self.index_path}' not found. Please create or load the index first.")

    def retrieve_context(self, query, k=3):
        docs = self.faiss_index.similarity_search(query, k=k)
        return "\n".join([doc.page_content for doc in docs])
