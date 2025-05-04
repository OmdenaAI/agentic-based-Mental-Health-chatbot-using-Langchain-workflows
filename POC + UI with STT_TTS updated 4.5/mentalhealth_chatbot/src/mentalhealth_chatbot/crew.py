from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from mentalhealth_chatbot.tools.custom_rag_tool import CustomRAGTool
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()

# ✅ Set Vertex AI credentials
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not google_credentials or not os.path.exists(google_credentials):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not found or invalid")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials

# ✅ Define the Vertex AI LLM
llm = LLM(
    model="gemini-1.5-flash",  # Model name for Vertex Gemini
    provider="vertexai",
    config={
        "project": "lucid-parsec-453323-n1",
        "location": "us-central1"
    }
)

# ✅ Initialize the custom RAG tool
rag_tool = CustomRAGTool()

@CrewBase
class MentalHealthChatbotCrew:
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # Agents
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
            tools=[rag_tool]
        )

    @agent
    def rag_reader(self) -> Agent:
        return Agent(config=self.agents_config["rag_reader"], llm=llm)

    # Tasks
    @task
    def emotion_detection_task(self) -> Task:
        return Task(config=self.tasks_config["emotion_detection_task"], output_file="logs/emotion_detection.md")

    @task
    def safety_check_task(self) -> Task:
        return Task(config=self.tasks_config["safety_check_task"], output_file="logs/safety_check.md")

    @task
    def rag_retrieval_task(self) -> Task:
        return Task(config=self.tasks_config["rag_retrieval_task"], output_file="logs/rag_retrieval.md")

    @task
    def rag_reading_task(self) -> Task:
        return Task(config=self.tasks_config["rag_reading_task"], output_file="logs/rag_reading.md")

    @task
    def suggestion_task(self) -> Task:
        return Task(config=self.tasks_config["suggestion_task"], output_file="logs/suggestion.md")

    @task
    def orchestrate_task(self) -> Task:
        return Task(config=self.tasks_config["orchestrate_task"], output_file="logs/orchestrate.md")

    # Crew definition
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            llm=llm  # ✅ Injected VertexAI LLM globally
        )
