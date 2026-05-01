
from agents.finance_agent import FinanceAgent
from agents.hr_agent import HRAgent
from agents.tech_agent import TechAgent
from rag.pipeline import RAGPipeline


class AgentFactory:
    def __init__(self, config, embeddings, llm):
        self.config = config
        self.embeddings = embeddings
        self.llm = llm

        self.agent_map = {
            "hr": HRAgent,
            "tech": TechAgent,
            "finance": FinanceAgent,
        }

    def create_agents(self):
        agents = {}

        for domain, agent_class in self.agent_map.items():
            pipeline = RAGPipeline(domain=domain, config=self.config)
            retriever = pipeline.build(embeddings=self.embeddings)

            agents[domain] = agent_class(
                retriever=retriever,
                llm=self.llm
            )

        return agents