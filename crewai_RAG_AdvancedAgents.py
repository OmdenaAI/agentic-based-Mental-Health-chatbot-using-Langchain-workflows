from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import PDFSearchTool,WebsiteSearchTool,SerperDevTool,CSVSearchTool
from dotenv import load_dotenv
import logging
import os
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
from litellm.exceptions import RateLimitError
import time
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]

# Create the pdf tool the data in the pdf will be read and stored in vectordb- chromadb
pdf_search_tool = PDFSearchTool(
    pdf="./manage_stress_workbook.pdf",
    config=dict(
        llm=dict(provider="huggingface", config=dict(model="distilbert-base-uncased")),  # Replace this with your desired Hugging Face model
        embedder=dict(
            provider="huggingface",
            config=dict(model="sentence-transformers/all-MiniLM-L6-v2")
        )
    ),
)

csv_search_tool = CSVSearchTool(pdf="./cleaned_data.csv",
    config=dict(
        llm=dict(provider="huggingface", config=dict(model="distilbert-base-uncased")),  # Replace this with your desired Hugging Face model
        embedder=dict(
            provider="huggingface",
            config=dict(model="sentence-transformers/all-MiniLM-L6-v2")
        )
    ),)

llm= LLM(
    model="groq/llama3-70b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key= GROQ_API_KEY
)
serper_tool = SerperDevTool()

web_search_tool = WebsiteSearchTool(config=dict(
        llm=dict(provider="huggingface", config=dict(model="distilbert-base-uncased")),  # Replace this with your desired Hugging Face model
        embedder=dict(
            provider="huggingface",
            config=dict(model="sentence-transformers/all-MiniLM-L6-v2")
        )
    ),)


advanced_question_generator = Agent(
    role="Advanced Mental Health Question Generator",
    goal=(
        "Guide users through a supportive mental health conversation but start the conversation based on {customer_question}"
        "Start a mental health conversation using the user's input: '{customer_question}'."
        "Generate personalized, context-aware mental health questions using insights from documents and the web. "
        "Adapt tone based on issue severity, emotion, and user sentiment."
    ),
    backstory=(
        "You're an intelligent question generator trained on psychological frameworks and supported by RAG + web data. "
        "You search through stress management materials and mental health sources online to form supportive questions."
        "and sharing feedback and support messages based on evaluated inputs."
    ),
    tools=[pdf_search_tool,serper_tool, web_search_tool,csv_search_tool],
    verbose=True,
    llm=llm,  # This is your Groq/LLama3 model
    allow_delegation=False
)

advanced_question_generator_task = Task(
    description=(
        "Initiate and manage the flow of the mental health conversation. "
        "After the user's response, evaluate the sentiment and context. "
        "Generate a mental health question using both retrieved document knowledge and web search. "
        "Base the question on the user's previous response, detected issue (e.g., anxiety, depression), and severity score if available. "
        "Ensure the question is supportive, context-aware, and encourages deeper reflection. "
        "If no issue is yet detected, ask a general wellness question sourced from mental health materials."
    ),
    expected_output=(
        "One well-formed mental health question tailored to the user's emotional state and previous response."
    ),
    agent=advanced_question_generator
)


crew = Crew(
    tasks=[advanced_question_generator_task],
    agents=[advanced_question_generator],
    # manager_agent=conversation_mediator_agent,  # This agent orchestrates everything
    process=Process.sequential  # Hierarchical lets the manager delegate
)

print("👋 Hi! I'm here to help you talk about your mental wellness. Let's get started.\n")

while True:
    print("if you don't want to continue the chat please enter quit or exit")
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("🧘 Thank you for sharing. Remember, you're not alone. Take care! 💛")
        break
    try:
    # Run the full conversation via the Conversation Mediator task
        result = crew.kickoff(inputs={"customer_question": user_input})
    except RateLimitError as e:
            print("Rate limit hit. Waiting 12 seconds...")
            time.sleep(12)
    print(f"🤖 Chatbot: {result}")




