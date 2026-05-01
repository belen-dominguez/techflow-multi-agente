"""
evaluator_agent.py
------------------
Responsabilidad: evaluar la calidad de la respuesta generada
por un agente RAG y registrar el puntaje en Langfuse.

"""
import json
from typing import Any, Dict

from sqlalchemy import text

from prompts.template import EVALUATOR_PROMPT


class EvaluatorAgent:
    """Evalúa la calidad de una respuesta RAG y envía los datos a Langfuse."""

    def __init__(
        self,
        llm: Any,

    ):
        """Inicializa el EvaluatorAgent.

        Args:
            llm: función o callable que recibe un prompt y retorna texto.
            
        """
        self.llm = llm


    def evaluate(self, query: str, answer: str) -> Dict:
        """Evalúa una respuesta y retorna los puntajes estructurados.

        Args:
           
            query: pregunta original del usuario.
            answer: respuesta generada por el agente RAG.
           
        Returns:
            Diccionario con los puntajes y explicación.
        """

        prompt = EVALUATOR_PROMPT.format(
            question=query,
            answer=answer,
        )

        response = self.llm.invoke(prompt)

        text  = response.content if hasattr(response, 'content') else str(response)
        return self._parse(text)

    def _parse(self, text: str) -> Dict:
            try:
                data = json.loads(text)
            except Exception:
                return {
                    "relevance": 0,
                    "accuracy": 0,
                    "completeness": 0,
                    "reasoning": text.strip()
                }

            return {
                "relevance": int(data.get("relevance", 0)),
                "accuracy": int(data.get("accuracy", 0)),
                "completeness": int(data.get("completeness", 0)),
                "reasoning": data.get("reasoning", "")
            }


