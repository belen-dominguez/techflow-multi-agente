"""
evaluator_agent.py
------------------
Responsabilidad: evaluar la calidad de la respuesta generada
por un agente RAG y registrar el puntaje en Langfuse.

Uso:
    from agents.evaluator_agent import EvaluatorAgent

    evaluator = EvaluatorAgent(llm=llm, langfuse_client=langfuse)
    evaluation = evaluator.evaluate(
        trace_id="abc123",
        query="¿Cuántos días de vacaciones tengo?",
        answer="TechFlow otorga 15 días hábiles por año...",
        chunks=[{"content": "...", "source": "..."}]
    )
"""
import json
from typing import Any, Callable, Dict, List, Optional

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






    # class EvaluatorAgent:
    # """Evalúa la calidad de una respuesta RAG y envía los datos a Langfuse."""

    # def __init__(
    #     self,
    #     llm: Any,

    # ):
    #     """Inicializa el EvaluatorAgent.

    #     Args:
    #         llm: función o callable que recibe un prompt y retorna texto.
            
    #     """
    #     self.llm = llm


    # def evaluate(self, query: str, answer: str, chunks=None) -> Dict:
    #     """Evalúa una respuesta y retorna los puntajes estructurados.

    #     Args:
           
    #         query: pregunta original del usuario.
    #         answer: respuesta generada por el agente RAG.
    #         chunks: lista de fragmentos recuperados, cada uno con 'content' y 'source'.
           
    #     Returns:
    #         Diccionario con los puntajes y explicación.
    #     """

    #     prompt = EVALUATOR_PROMPT.format(
    #         question=query,
    #         answer=answer,
    #     )

    #     response = self.llm.invoke(prompt)

    #     text  = response.content if hasattr(response, 'content') else str(response)    
    #     evaluation = self._parse_evaluation(raw_response)

    #     if evaluation.get("final_score") is None:
    #         evaluation["final_score"] = self._compute_final_score(
    #             evaluation.get("relevance"),
    #             evaluation.get("accuracy"),
    #             evaluation.get("completeness"),
    #         )

    #     if save_score and self.langfuse_client is not None:
    #         self._send_langfuse_score(trace_id=trace_id, evaluation=evaluation)

    #     return evaluation

    # def _format_chunks(self, chunks: List[Dict[str, str]]) -> str:
    #     formatted = []
    #     for index, chunk in enumerate(chunks, start=1):
    #         content = chunk.get("content", "")
    #         source = chunk.get("source", "unknown")
    #         formatted.append(f"Fragmento {index}: {content}\nFuente: {source}")
    #     return "\n\n".join(formatted)

    # def _parse_evaluation(self, raw_response: str) -> Dict[str, Any]:
    #     try:
    #         parsed = json.loads(raw_response)
    #         return {
    #             "relevance": int(parsed.get("relevance", 0)),
    #             "accuracy": int(parsed.get("accuracy", 0)),
    #             "completeness": int(parsed.get("completeness", 0)),
    #             "final_score": int(parsed.get("final_score", 0))
    #             if parsed.get("final_score") is not None
    #             else None,
    #             "reason": parsed.get("reason", ""),
    #         }
    #     except json.JSONDecodeError:
    #         return self._fallback_parse(raw_response)

    # def _fallback_parse(self, raw_response: str) -> Dict[str, Any]:
    #     values = {
    #         "relevance": 0,
    #         "accuracy": 0,
    #         "completeness": 0,
    #         "final_score": None,
    #         "reason": raw_response.strip().replace("\n", " "),
    #     }

    #     for key in ["relevance", "accuracy", "completeness", "final_score"]:
    #         if key in raw_response:
    #             try:
    #                 token = raw_response.split(key)[1].strip().split()[0].strip(":, ")
    #                 values[key] = int(token)
    #             except (IndexError, ValueError):
    #                 continue

    #     return values

    # def _compute_final_score(
    #     self,
    #     relevance: Optional[int],
    #     accuracy: Optional[int],
    #     completeness: Optional[int],
    # ) -> int:
    #     scores = [score for score in (relevance, accuracy, completeness) if score is not None]
    #     if not scores:
    #         return 0
    #     return round(sum(scores) / len(scores))

    # def _send_langfuse_score(self, trace_id: str, evaluation: Dict[str, Any]) -> None:
    #     payload = {
    #         "trace_id": trace_id,
    #         "relevance": evaluation.get("relevance"),
    #         "accuracy": evaluation.get("accuracy"),
    #         "completeness": evaluation.get("completeness"),
    #         "final_score": evaluation.get("final_score"),
    #         "reason": evaluation.get("reason"),
    #     }

    #     client = self.langfuse_client
    #     if hasattr(client, "score"):
    #         client.score(trace_id=trace_id, score=payload.get("final_score"), metadata=payload)
    #     elif hasattr(client, "log"):
    #         client.log("evaluation", payload)
    #     else:
    #         print(f"[EvaluatorAgent] Cliente Langfuse sin método compatible. Payload: {payload}")
