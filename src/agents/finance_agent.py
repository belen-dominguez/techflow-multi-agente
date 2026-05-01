"""
finance_agent.py
----------------
Responsabilidad: responder consultas sobre Finanzas
usando RAG sobre la documentación interna de Finance de TechFlow.

"""
from typing import Any, Dict

from prompts.template import RAG_AGENT_PROMPT

DOMAIN_NAME = "Finanzas (Finance)"

class FinanceAgent:
    """Agente especializado en consultas de Finanzas.

    Recupera chunks de la base de conocimiento de Finance
    y genera respuestas fundamentadas en esa documentación.
    """

    def __init__(self, retriever: Any, llm: Any):
        """Inicializa el agente con el retriever y el LLM."""
        self.retriever = retriever
        self.llm = llm

    def answer(self, question: str) -> Dict:
        """Responde una pregunta usando el retriever y el modelo de lenguaje."""
        # Recupera los documentos más relevantes
        chunks = self.retriever.retrieve(question)

        # Construye un prompt simple con los documentos y la pregunta
        context = "\n\n".join(chunk.page_content for chunk in chunks)
        prompt = RAG_AGENT_PROMPT.format(
                domain=DOMAIN_NAME,
                context=context,
                question=question,
            )

        response = self.llm.invoke(prompt)
        print(f"[FinanceAgent] Respondiendo: '{response.content if hasattr(response, 'content') else str(response)}'")   
        return {"response": response.content if hasattr(response, 'content') else str(response), "prompt": prompt, }
