"""
hr_agent.py
-----------
Responsabilidad: responder consultas sobre Recursos Humanos
usando RAG sobre la documentación interna de HR de TechFlow.


"""


from agents.base_agent import BaseRAGAgent
from prompts.template import RAG_AGENT_PROMPT
from shared.logger import get_logger

DOMAIN_NAME = "Recursos Humanos (HR)"
log = get_logger("hr_agent")

class HRAgent(BaseRAGAgent):
    def __init__(self, retriever, llm):
        super().__init__(
            retriever=retriever,
            llm=llm,
            domain_name=DOMAIN_NAME,
            logger=log
        )