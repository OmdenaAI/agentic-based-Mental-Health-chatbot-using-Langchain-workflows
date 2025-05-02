from crewai.tools import BaseTool
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from typing import Any


class CustomRAGTool(BaseTool):
    name: str = "Custom RAG Tool"
    description: str = "Retrieves relevant mental health tips from a text corpus using LangChain and FAISS."
    vector_store: Any = None
    
    def __init__(self):
        super().__init__()
        # Load and process corpus
        self.vector_store = self._build_vector_store()
        
    def _build_vector_store(self):
        """Load, split, embed, and store documents from knowledge base."""
        documents = []
        knowledge_base_dir = "knowledge"

        # Load files
        for file in os.listdir(knowledge_base_dir):
            file_path = os.path.join(knowledge_base_dir, file)
            try:
                if file.endswith(".txt"):
                    loader = TextLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                elif file.endswith(".csv"):
                    loader = CSVLoader(file_path, encoding="utf-8")
                    documents.extend(loader.load())
            except Exception as e:
                print(f"Warning: Failed to load {file}: {e}")
        
        # Split into chunks (small for simplicity)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=20
        )
        chunks = text_splitter.split_documents(documents)

        # Create embeddings with Gemini
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

        # Store in FAISS vector store
        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store
    
    
    def _run(self, query: str) -> str:
        """Retrieve relevant chunks for the query."""
        # Search for top 3 relevant chunks
        results = self.vector_store.similarity_search(query, k=3)
        # Combine retrieved chunks into a single string
        retrieved_text = "\n".join([doc.page_content for doc in results])
        print(f"Retrieved tips: {retrieved_text}")  # Debug logging
        return retrieved_text if retrieved_text else "No relevant tips found."
    