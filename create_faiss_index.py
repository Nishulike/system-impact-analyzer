from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

load_dotenv()

# Sample documents (you can replace these with your system impact documents)
docs = [
    Document(page_content="The CRM system collects customer data and preferences."),
    Document(page_content="The underwriting module uses risk data to evaluate policies."),
    Document(page_content="The claims module processes insurance claims for customers."),
]

# Initialize embeddings using Google Gemini
embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# Create FAISS index
faiss_index = FAISS.from_documents(docs, embedding)

# Save index to local directory
index_path = "faiss_index_dir"
faiss_index.save_local(index_path)

print("✅ FAISS index created and saved to:", index_path)
