"""
finance_agent.py
----------------
Responsabilidad: responder consultas sobre Finanzas
usando RAG sobre la documentación interna de Finance de TechFlow.

"""

from agents.base_agent import BaseRAGAgent
from prompts.template import RAG_AGENT_PROMPT
from shared.logger import get_logger


DOMAIN_NAME = "Finanzas (Finance)"
log = get_logger("finance_agent")

class FinanceAgent(BaseRAGAgent):
    def __init__(self, retriever, llm):
        super().__init__(
            retriever=retriever,
            llm=llm,
            domain_name=DOMAIN_NAME,
            logger=log
        )