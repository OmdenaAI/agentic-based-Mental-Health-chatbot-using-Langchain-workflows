from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import os
from  mental_health_chat_bot.tools.custom_rag_tool import CustomRAGTool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv


# # Load environment variables
load_dotenv()

# Verify Gemini API key
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")
os.environ["GOOGLE_API_KEY"] = google_api_key

# Verify Google Application Credentials
google_credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not google_credentials or not os.path.exists(google_credentials):
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS not found or invalid")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials


# Initialize custom RAG tool
rag_tool = CustomRAGTool()

@CrewBase
class MentalHealthChatbotCrew:
    """MentalHealthChatbot crew"""
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def emotion_detector(self) -> Agent:
        return Agent(config=self.agents_config["emotion_detector"])

    @agent
    def suggestion_agent(self) -> Agent:
        return Agent(config=self.agents_config["suggestion_agent"])

    @agent
    def safety_agent(self) -> Agent:
        return Agent(config=self.agents_config["safety_agent"])

    @agent
    def orchestrator(self) -> Agent:
        return Agent(config=self.agents_config["orchestrator"])
    
    
    @agent
    def rag_retriever(self) -> Agent:
        config = self.agents_config["rag_retriever"]
        return Agent(
            role=config["role"],
            goal=config["goal"],
            backstory=config["backstory"],
            memory=config["memory"],
            verbose=config["verbose"],
            llm=config["llm"],
            tools=[rag_tool]  # Pass instantiated tool directly
        )
    
    @agent
    def rag_reader(self) -> Agent:
        return Agent(config=self.agents_config["rag_reader"])
    

    @task
    def emotion_detection_task(self) -> Task:
        return Task(config=self.tasks_config["emotion_detection_task"],
                    output_file="logs/emotion_detection.md")

    @task
    def safety_check_task(self) -> Task:
        return Task(config=self.tasks_config["safety_check_task"],
                    output_file="logs/safety_check.md")
        
    
    @task
    def rag_retrieval_task(self) -> Task:
        return Task(
            config=self.tasks_config["rag_retrieval_task"],
            output_file="logs/rag_retrieval.md"
        )
    
    
    @task
    def rag_reading_task(self) -> Task:
        return Task(
            config=self.tasks_config["rag_reading_task"],
            output_file="logs/rag_reading.md"
        )
    

    @task
    def suggestion_task(self) -> Task:
        return Task(config=self.tasks_config["suggestion_task"],
                   output_file="logs/suggestion.md")

    @task
    def orchestrate_task(self) -> Task:
        return Task(config=self.tasks_config["orchestrate_task"],
                    output_file="logs/orchestrate.md")

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False,
            planning=True,
            planning_llm="gemini-1.5-flash",
        )