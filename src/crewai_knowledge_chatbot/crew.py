from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.knowledge.source.pdf_knowledge_source import PDFKnowledgeSource
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

# Create a PDF knowledge source
pdf_source = PDFKnowledgeSource(file_paths=["CoALA.pdf"])

memory_config = {
  "provider": "mem0",
	 "config": {"user_id": "User"},
}

@CrewBase
class CrewaiKnowledgeChatbot():
    """CrewaiKnowledgeChatbot crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def assistant(self) -> Agent:
        return Agent(
            config=self.agents_config['assistant'],
            memory=True,
            memory_config=memory_config,
            verbose=False,
        )

    
    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def chat_task(self) -> Task:
        return Task(
            config=self.tasks_config["chat_task"],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiKnowledgeChatbot crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            knowledge_sources=[pdf_source],
            verbose=False,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )