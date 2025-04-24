from crewai.tools import BaseTool
from langchain_community.document_loaders import TextLoader
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
        """Load, split, embed, and store documents in FAISS."""
        # Load text file
        loader = TextLoader("mental_health_tips.txt")
        documents = loader.load()
        
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
        # Search for top 2 relevant chunks
        results = self.vector_store.similarity_search(query, k=2)
        # Combine retrieved chunks into a single string
        retrieved_text = "\n".join([doc.page_content for doc in results])
        return retrieved_text if retrieved_text else "No relevant tips found."
    