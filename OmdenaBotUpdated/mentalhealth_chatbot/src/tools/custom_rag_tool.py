import os
from crewai.tools import BaseTool
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from typing import Any

class CustomRAGTool(BaseTool):
    name: str = "Custom RAG Tool"
    description: str = "Retrieves relevant mental health tips from documents using LangChain and FAISS."
    vector_store: Any = None

    def __init__(self):
        super().__init__()

    def _build_vector_store(self):
        documents = []

        # ✅ Absolute path to correct folder
        knowledge_base_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "knowledge")
        )

        if not os.path.exists(knowledge_base_dir):
            raise FileNotFoundError(f"❌ Knowledge folder not found at {knowledge_base_dir}")

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
                print(f"⚠️ Warning: Failed to load {file}: {e}")

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=50
        )
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store

    def _run(self, query: str) -> str:
        if self.vector_store is None:
            self.vector_store = self._build_vector_store()

        results = self.vector_store.similarity_search(query, k=1)
        retrieved_text = "\n".join([doc.page_content for doc in results])
        if retrieved_text:
            print(f"[CustomRAGTool] ✅ Retrieved relevant text for query: {query}")
        else:
            print(f"[CustomRAGTool] ❌ No relevant text found for query: {query}")
        return retrieved_text if retrieved_text else "No relevant tips found."
