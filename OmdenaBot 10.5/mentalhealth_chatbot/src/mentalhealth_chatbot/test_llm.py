from crewai import LLM
import os
from dotenv import load_dotenv

load_dotenv()

llm = LLM(
    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
    provider="openai",
    config={"api_key": os.getenv("OPENAI_API_KEY")}
)

response = llm.complete("Say hi")
print("✅ LLM Response:", response)
