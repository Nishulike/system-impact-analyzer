from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os


class FaissStore:
    def __init__(self, index_path: str = "faiss_index_dir"):    
        """
        Initialize FaissStore by loading an existing FAISS index.
        
        Args:
            index_path (str): Directory path where the FAISS index is stored.
        
        Raises:
            FileNotFoundError: If index_path does not exist.
            RuntimeError: If loading the index fails.
        """
        self.index_path = index_path
        self.faiss_index = None
        
        try:
            self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")  # Gemini embedding model
        except Exception as e:
            raise RuntimeError(f"Failed to initialize embeddings: {e}")
        
        if os.path.exists(self.index_path):
            try:
                self.faiss_index = FAISS.load_local(
                    self.index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True  # ✅ Required for loading index.pkl
                )
            except Exception as e:
                raise RuntimeError(f"Failed to load FAISS index from '{self.index_path}': {e}")
        else:
            raise FileNotFoundError(
                f"FAISS index directory '{self.index_path}' not found. "
                "Please create or load the index first."
            )
    
    def retrieve_context(self, query: str, k: int = 3) -> str:
        """
        Retrieve top-k similar documents' content based on the query.
        
        Args:
            query (str): The query string to search for.
            k (int): Number of top results to return.
        
        Returns:
            str: Concatenated string of document contents; empty string if no results.
        """
        if not self.faiss_index:
            raise RuntimeError("FAISS index is not loaded.")
        
        docs = self.faiss_index.similarity_search(query, k=k)
        if not docs:
            return ""
        
        return "\n".join(doc.page_content for doc in docs)
