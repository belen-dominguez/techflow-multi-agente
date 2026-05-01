"""
hr_agent.py
-----------
Responsabilidad: responder consultas sobre Recursos Humanos
usando RAG sobre la documentación interna de HR de TechFlow.

Uso:
    from agents.hr_agent import HRAgent

    agent = HRAgent(retriever=retriever, llm=llm)
    result = agent.answer("¿Cuántos días de vacaciones tengo?")
"""

from typing import Any, Dict
from urllib import response

from prompt_toolkit import prompt

from prompts.template import RAG_AGENT_PROMPT

DOMAIN_NAME = "Recursos Humanos (HR)"

class HRAgent:
    """Agente especializado en consultas de Recursos Humanos.

    Recupera chunks de la base de conocimiento de HR
    y genera respuestas fundamentadas en esa documentación.
    """

    def __init__(self, retriever: Any, llm: Any):
        """Inicializa el agente con el retriever y el LLM."""
        self.retriever = retriever
        self.llm = llm

    def answer(self, question: str) -> Dict:
        """Responde una pregunta usando el retriever y el modelo de lenguaje."""
        
        chunks = self.retriever.retrieve(question)

        # Construye un prompt simple con los documentos y la pregunta
        context = "\n\n".join(chunk.page_content for chunk in chunks)
        prompt = RAG_AGENT_PROMPT.format(
                domain=DOMAIN_NAME,
                context=context,
                question=question,
            )

        response = self.llm.invoke(prompt)

        print(f"[HRAgent] Respondiendo: '{response.content if hasattr(response, 'content') else str(response)}'")   
        return {"response": response.content if hasattr(response, 'content') else str(response), "prompt": prompt, }
