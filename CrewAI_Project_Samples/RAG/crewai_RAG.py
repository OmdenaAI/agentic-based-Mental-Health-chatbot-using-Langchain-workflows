from crewai import Agent, Crew, Process, Task, LLM
from crewai_tools import PDFSearchTool,WebsiteSearchTool
from dotenv import load_dotenv
import logging
import os
from transformers import pipeline
from transformers import AutoModelForCausalLM, AutoTokenizer
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


llm= LLM(
    model="groq/llama3-70b-8192",
    base_url="https://api.groq.com/openai/v1",
    api_key= GROQ_API_KEY
)

web_search_tool = WebsiteSearchTool(config=dict(
        llm=dict(provider="huggingface", config=dict(model="distilbert-base-uncased")),  # Replace this with your desired Hugging Face model
        embedder=dict(
            provider="huggingface",
            config=dict(model="sentence-transformers/all-MiniLM-L6-v2")
        )
    ),)

research_agent = Agent(
    role="Mental Health Research Agent", 
    goal="Search through the PDF to find relevant answers",
    allow_delegation=False,
    verbose=True,
    backstory=(
        """
        The research agent is adept at searching and 
        extracting data from documents , ensuring accurate and prompt responses related to customers questions on mental health.
        """
    ),
    llm=llm,
    tools=[pdf_search_tool,web_search_tool],
)


answer_customer_question_task = Task(
    description=(
        """
        Answer the customer's questions based on the Mental Health PDF.
        The research agent will search through the PDF and web to find the relevant answers.
        Your final answer MUST be clear and accurate, based on the content of the Mental Helath PDF.

        Here is the customer's question:
        {customer_question}
        """
    ),
    expected_output="""
        Provide clear and accurate answers to the customer's questions based on 
        the content of the Mental Health PDF.
        """,
    tools=[pdf_search_tool,web_search_tool],
    agent=research_agent,
)

crew = Crew(
    tasks=[answer_customer_question_task],
    agents=[research_agent],
    process=Process.sequential,
)

customer_question = input(
    "What is your question?  "
)

try:
    result = crew.kickoff(inputs={"customer_question": customer_question})
# print(result)
except ValueError as e:
    if "Invalid response from LLM call" in str(e):
        print("Sorry, I don't have answer for that question")
        # Optional: handle fallback here
    else:
        raise
 


