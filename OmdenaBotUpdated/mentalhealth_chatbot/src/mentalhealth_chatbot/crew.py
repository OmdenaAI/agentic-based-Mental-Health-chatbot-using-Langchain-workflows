import os
import socket
from dotenv import load_dotenv

from crewai import Agent, Task, LLM, Crew
from crewai.project import CrewBase, agent, task

from tools.custom_rag_tool import CustomRAGTool
from tools.custom_tool import MyCustomTool

import yaml


load_dotenv()

# --- Connectivity check ---
def is_online():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False

# --- LLM Selection ---
from crewai import LLM
import litellm

def get_llm():
    if is_online() and os.getenv("OPENAI_API_KEY"):
        print("✅ Using OpenAI (online)")

        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

        return LLM(
            model="gpt-3.5-turbo",
            api_key=os.getenv("OPENAI_API_KEY"),
            temperature=0.7
        )
    else:
        print("⚠️ No internet or OpenAI key. Using Ollama (offline)")
        return LLM(
            model=os.getenv("OLLAMA_MODEL", "llama3"),
            base_url="http://localhost:11434"
        )

llm = get_llm()

# --- Load tools ---
rag_tool = CustomRAGTool()
custom_tool = MyCustomTool()

# --- CrewAI Base Class ---
@CrewBase
class MentalHealthChatbotCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    # --- Agents ---
    @agent
    def emotion_detector(self) -> Agent:
        return Agent(config=self.agents_config["emotion_detector"], llm=llm)

    @agent
    def suggestion_agent(self) -> Agent:
        return Agent(config=self.agents_config["suggestion_agent"], llm=llm)

    @agent
    def safety_agent(self) -> Agent:
        return Agent(config=self.agents_config["safety_agent"], llm=llm)

    @agent
    def orchestrator(self) -> Agent:
        return Agent(config=self.agents_config["orchestrator"], llm=llm)

    @agent
    def rag_retriever(self) -> Agent:
        config = self.agents_config["rag_retriever"]
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            memory=config["memory"],
            verbose=config["verbose"],
            llm=llm,
            tools=[rag_tool, custom_tool]
        )

    @agent
    def rag_reader(self) -> Agent:
        return Agent(config=self.agents_config["rag_reader"], llm=llm)

    # --- Tasks ---
    @task
    def emotion_detection_task(self) -> Task:
        return Task(config=self.tasks_config["emotion_detection_task"])

    @task
    def safety_check_task(self) -> Task:
        return Task(config=self.tasks_config["safety_check_task"])

    @task
    def rag_retrieval_task(self) -> Task:
        return Task(config=self.tasks_config["rag_retrieval_task"])

    @task
    def rag_reading_task(self) -> Task:
        return Task(config=self.tasks_config["rag_reading_task"])

    @task
    def suggestion_task(self) -> Task:
        return Task(config=self.tasks_config["suggestion_task"])

    @task
    def orchestrate_task(self) -> Task:
        return Task(config=self.tasks_config["orchestrate_task"])
    
    @task
    def profile_feedback_task(self) -> Task:
        return Task(config=self.tasks_config["profile_feedback_task"])


    # ✅ Add this crew() method so .kickoff() will work
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.rag_retriever(),
                self.rag_reader(),
                self.orchestrator()
            ],
            tasks=[
                self.rag_retrieval_task(),
                self.rag_reading_task(),
                self.orchestrate_task(),
                self.profile_feedback_task(),  # ✅ Add this
            ],
            verbose=True
        )