
from llama_index.core import VectorStoreIndex, ServiceContext, StorageContext, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.schema import Document
from llama_index.core.schema import QueryBundle
from llama_index.core.schema import NodeWithScore

import chromadb
import os
import pandas as pd
from autogen import AssistantAgent, UserProxyAgent
from autogen import GroupChat, GroupChatManager
from autogen.oai.groq import GroqClient
#from rag_pipeline import load_and_split_csv, build_faiss_index
from llama_index.core.query_engine import RetrieverQueryEngine
from dotenv import load_dotenv
load_dotenv()

os.environ['GEMINI_API_KEY']=os.getenv("GEMINI_API_KEY")
os.environ['SERPAPI_API_KEY']=os.getenv("SERPAPI_API_KEY")
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")


from serpapi import GoogleSearch

class WebSearchAgent:
    def __init__(self, api_key):
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("SERPAPI_API_KEY not set in environment variables.")

    def search(self, query):
        params = {
            "engine": "google",
            "q": query,
            "api_key": self.api_key,
        }
        print(f"Searching web with SerpAPI for: {query}")
        search = GoogleSearch(params)
        results = search.get_dict()
        organic = results.get("organic_results", [])

        if organic:
            top_results = "\n\n".join(
                f"{i+1}. {r['title']}\n{r['snippet']}" 
                for i, r in enumerate(organic[:3])
            )
            return f"Top Web Results:\n\n{top_results}"
        else:
            return "No relevant web information found."


# class MentalHealthRetriever:
#      def __init__(self):
#         self.embeddings = OllamaEmbeddings(model="llama3.2:1b")

#         try:
#             self.db = FAISS.load_local("mental_health_db", self.embeddings)
#             print("Loaded existing mental health database")
#         except:
#             print("Creating new mental health database...")
#             loader = CSVLoader(file_path="DataSet/labeled_with_severity_nuanced.csv")
#             documents = loader.load()
#             text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#             texts = text_splitter.split_documents(documents)
#             self.db = FAISS.from_documents(texts, self.embeddings)
#             self.db.save_local("mental_health_db")
#             print("Database created and saved")

#      def retrieve_docs(self, query: str) -> str:
#         print(f"Retrieving documents for query: {query}")
#         retriever = self.db.as_retriever(search_kwargs={"k": 5})
#         docs = retriever.get_relevant_documents(query)
#         result = "\n\n".join([f"Document {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
#         print(f"Retrieved {len(docs)} documents")
#         return result 

class MentalHealthRetriever:
    def __init__(self):
        # Step 1: Gemini Model
        Settings.embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
        llm = Gemini(model="models/gemini-1.5-flash", temperature=0.7)
    
        # Step 2: Embedding model is required for Chroma (LlamaIndex will default if not set manually)
        self.persist_dir = "mental_health_chroma_db"
        self.collection_name = "mental_health"

        # Step 3: Load or Create Chroma Vector DB
        chroma_client = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = chroma_client.get_or_create_collection(name=self.collection_name)
        vector_store = ChromaVectorStore(
            chroma_collection=chroma_collection,
            persist_dir=self.persist_dir
        )

        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

        if len(chroma_collection.get()["ids"]) > 0:
            print("Loaded existing ChromaDB.")
            self.index=VectorStoreIndex.from_vector_store(vector_store=vector_store,show_progress=True)
        else:
            print("No existing DB found. Creating from CSV...")
            df = pd.read_csv("labeled_with_severity_nuanced.csv")
            documents = [Document(text=row["text"]) for _, row in df.iterrows()]
            parser = SentenceSplitter(chunk_size=1000, chunk_overlap=100)
            nodes = parser.get_nodes_from_documents(documents)

            self.index = VectorStoreIndex(
                nodes,
                storage_context=self.storage_context
            )
            print("Index built and saved.")

    def retrieve_docs(self, query: str) -> str:
        print(f"Retrieving documents for query: {query}")
        retriever = self.index.as_retriever(similarity_top_k=5)
        docs = retriever.retrieve(query)
        if docs and any(doc.text.strip() for doc in docs):
            combined = "\n\n".join([f"Document {i+1}:\n{doc.text}" for i, doc in enumerate(docs)])
            print("Found local documents. Returning response.")
            return self.rewrite_empathically(combined)
        else:
            print("No relevant documents found locally. Switching to web search.")
            web_result = self.web_agent.search(query)
            return self.rewrite_empathically(web_result)

    def retrieve(self, query_bundle: QueryBundle) -> list[NodeWithScore]:
        retriever = self.index.as_retriever(similarity_top_k=5)
        return retriever.retrieve(query_bundle)

    def rewrite_empathically(self, answer):
        prompt = f"""
        Rephrase the following response to sound empathetic and supportive, suitable for a person experiencing mental stress:

        Original: "{answer}"

        Empathetic Response:
        """
        return prompt


config_list = [{
    "model": "llama-3.1-8b-instant",
    "api_key": os.getenv("GROQ_API_KEY"),
    "api_type": "groq"
}]


retriever_tool = MentalHealthRetriever()
query_engine = RetrieverQueryEngine.from_args(
    retriever=retriever_tool,
    llm = Gemini(model="models/gemini-1.5-flash", temperature=0.7),
    response_mode="compact"
)

retriever_agent = AssistantAgent(
    name="Retriever-Agent",
    system_message="""You are a specialized retrieval agent for mental health data. 
    For ALL questions, you MUST use your knowledge.
    NEVER try to answer questions directly without first retrieving information from your knowledge base.
    After retrieving information, summarize the common themes or patterns in the retrieved documents.
    """,
    llm_config={
        "config_list": config_list,
        "functions": [
            {
                "name": "retrieve_docs",
                "description": "Retrieves mental health documents relevant to the query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The search query about mental health topics"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    },
    function_map={"retrieve": retriever_tool.retrieve_docs}
)

empathy_agent = AssistantAgent(
    name="Empathy-Agent",
    system_message=""" You are an empathetic assistant. Rewrite responses to be warm, supportive, and encouraging.""",
    llm_config={
        "config_list": config_list,
        "functions": [
            {
                "name": "rewrite_empathically",
                "description": "Rewrites a response to be more empathetic and supportive for mental health contexts",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "answer": {
                            "type": "string",
                            "description": "The original response to be rephrased with empathy"
                        }
                    },
                    "required": ["answer"]
                }
            }
        ]
    },
    function_map={"rewrite_empathically": retriever_tool.rewrite_empathically}
)

user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False} # Set to True if you want to use Docker for code execution (By default its true, hence need to specify when running in local machine)
)

web_search_agent = WebSearchAgent(api_key=os.getenv("SERPAPI_API_KEY"))

# group_chat = GroupChat(
#     agents=[user_proxy, retriever_agent, empathy_agent],
#     messages=[],
#     max_round=5
# )

# manager = GroupChatManager(
#     groupchat=group_chat,
#     llm_config={"config_list": config_list}
# )


# user_proxy.initiate_chat(
#     manager,
#     message="What are the most common triggers mentioned in anxiety posts according to you?"
# )

# def ensure_index_exists(index_dir="vector_store/", data_path="data/labeled_with_severity_nuanced.csv"):
#     if not os.path.exists(index_dir) or not os.listdir(index_dir):
#         print("⚠️ Index not found. Building a new one from dataset...")
#         nodes = load_and_split_csv(csv_path=data_path)
#         build_faiss_index(nodes, index_save_dir=index_dir)
#     else:
#         print("✅ FAISS index already exists. Skipping index creation.")

def handle_user_query(query: str) -> str:
    """
    Attempts to answer using LlamaIndex.
    Falls back to AutoGen agents if knowledge base yields nothing.
    """
    print(f"Received query from UI: {query}")
    # Step 1: Try LlamaIndex
    #query_engine = index.as_query_engine()
    response = query_engine.query(query)
    response_text = str(response).strip()

    if response_text.lower().startswith("i don't know") or len(response_text) < 20:
        # Step 2: Fall back to group agent chat
        print("No good match in LlamaIndex. Falling back to AutoGen.")
        groupchat = GroupChat(
            agents=[user_proxy, retriever_agent, web_search_agent, empathy_agent],
            messages=[{"role": "user", "content": query}],
            max_round=5
        )
        manager = GroupChatManager(groupchat=groupchat, llm_config={"config_list": config_list})
        result = manager.run()
        return str(result.summary)

    print("Answered via LlamaIndex.")
    return response_text



