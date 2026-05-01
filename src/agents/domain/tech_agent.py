"""
tech_agent.py
-------------
Responsabilidad: responder consultas sobre IT y Tecnología
usando RAG sobre la documentación interna de Tech de TechFlow.

"""

from agents.base.base_agent import BaseRAGAgent
from prompts.template import RAG_AGENT_PROMPT
from shared.logger import get_logger

DOMAIN_NAME = "Tecnología (Tech)"
log = get_logger("tech_agent")

class TechAgent(BaseRAGAgent):
    def __init__(self, retriever, llm):
        super().__init__(
            retriever=retriever,
            llm=llm,
            domain_name=DOMAIN_NAME,
            logger=log
        )