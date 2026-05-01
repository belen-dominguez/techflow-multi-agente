"""
tracer.py
---------
Responsabilidad: instrumentar el flujo del sistema con Langfuse v4.

Uso:
    from shared.tracer import TracedOrchestrator

    traced = TracedOrchestrator(orchestrator=orchestrator)
    result = traced.route("¿Cuántos días de vacaciones tengo?")
"""
import uuid
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from langfuse import Langfuse


load_dotenv()

class Tracer:
    def __init__(self):
        self.client = Langfuse()
        self.trace = None

    # iniciar trace
    def start_trace(self, name: str,  input_data: dict):
        return self.client.start_as_current_observation(
        name=name,
        input=input_data
        )
    

    # crear span
    def start_span(self, name: str, input_data: dict = None):
        return self.client.start_as_current_observation(
            name=name,
            input=input_data
        )
      
    
    # guardar output final
    def set_output(self, output_data: dict):
        self.client.update_current_span(output=output_data)

      
    # guardar scores
    def add_score(self,trace_id: str, name: str, value: float, comment: str = None):
          self.client.create_score(
                trace_id=trace_id,
                name=name,
                value=value,
                comment=comment,
            )


# no creo score pero lo deja en output. scrore no esta funcionando bien
          self.client.update_current_span(
                output={
                    "score_name": name,
                    "score_value": value,
                    "score_comment": comment
                }
            )
      
    # fuerza el envío inmediato de todo
    def flush(self):
        self.client.flush()

# class TracedOrchestrator:
    # """Envuelve al Orchestrator y registra cada consulta en Langfuse."""

    # def __init__(
    #     self,
    #     orchestrator: Any,
    # ):
    #     """Inicializa el wrapper de trazado.

    #     Args:
    #         orchestrator: instancia de Orchestrator a envolver.
    #     """
    #     self.orchestrator = orchestrator
    #     self.langfuse = None
    #     self._enabled = False
    #     self.trace_id = None

    #     try:
    #         self.langfuse = Langfuse()
    #         self._enabled = True
    #         print("[TracedOrchestrator] Langfuse conectado.")
    #     except Exception as e:
    #         print(f"[TracedOrchestrator] Langfuse no disponible: {e}")
    #         self._enabled = False

    # def route(self, question: str, trace_id: Optional[str] = None) -> str:
    #     """Enruta la consulta y registra la traza en Langfuse.

    #     Si Langfuse no está disponible, el enrute continúa igual.
    #     """
    #     trace_id = trace_id or self._create_trace_id()
    #     # self._log_request(trace_id, question)

    #     if self._enabled:
    #         try:
    #             with self.langfuse.start_as_current_observation(
    #                     name="multiagent-query",
    #                     input={"query": question}
    #                 ):
    #                     # Ejecutamos el orchestrator dentro del contexto del trace
    #                     result = self.orchestrator.route(question)
                        
    #                     # Actualizamos el output del trace
    #                     self.langfuse.update_current_span(output={
    #                         "domain": result.get("domain"),
    #                         "answer": result.get("answer", ""),
    #                         "routed_by": result.get("routed_by", ""),
    #                     })

    #                     result["trace_id"] = self.langfuse.get_current_trace_id()
    #             # result = self.orchestrator.route(question)
    #             # answer = result["answer"]
    #             # self._log_response(trace_id, question, answer, success=True)
    #             # return result
    #         except Exception as error:
    #             self._log_response(
    #                 trace_id,
    #                 question,
    #                 str(error),
    #                 success=False,
    #                 error=str(error),
    #             )
    #             raise

    # def _create_trace_id(self) -> str:
    #     return uuid.uuid4().hex

    # def _log_request(self, trace_id: str, question: str) -> None:
    #     payload = {
    #         "trace_id": trace_id,
    #         "event": "orchestrator.request",
    #         "question": question,
    #     }
    #     self._send_langfuse(payload)

    # def _log_response(
    #     self,
    #     trace_id: str,
    #     question: str,
    #     answer: str,
    #     success: bool,
    #     error: Optional[str] = None,
    # ) -> None:
    #     payload: Dict[str, Any] = {
    #         "trace_id": trace_id,
    #         "event": "orchestrator.response",
    #         "question": question,
    #         "answer": answer,
    #         "success": success,
    #     }

    #     if error is not None:
    #         payload["error"] = error

    #     # self._send_langfuse(trace_id)

    # def _send_langfuse(self, trace_id: str, name: str, value: float, comment: str = "") -> None:
    #     #  def score(self, trace_id: str, name: str, value: float, comment: str = "") -> None:
    #     """
    #     Envía un score a Langfuse asociado a un trace.
    #     Lo usa el EvaluatorAgent para registrar la calidad de las respuestas.

    #     Args:
    #         trace_id: ID del trace al que asociar el score.
    #         name:     nombre del score (ej: "final_score", "relevance").
    #         value:    valor numérico del score.
    #         comment:  justificación opcional.
    #     """
    #     if not self._enabled:
    #         return

    #     try:
    #         self.langfuse.create_score(
    #             trace_id=trace_id,
    #             name=name,
    #             value=value,
    #             comment=comment,
    #         )
    #     except Exception as e:
    #         print(f"[TracedOrchestrator] Error al registrar score: {e}")

    #     # if self.langfuse is None:
    #     #     return


    #     # client = get_client()

    #     # try:
    #     #     # trace_method = getattr(client, "trace", None)
    #     #     # if trace_method:
    #     #     #     trace_method(
    #     #     #         name=payload.get("event", "orchestrator"),
    #     #     #         input=payload,
    #     #     #     )
    #     #     # else:
    #     #     #     print(f"[TracedOrchestrator] Método trace no disponible en Langfuse: {payload}")
    #     #     for score_name, score_value in payload.items():
    #     #         print(f"wwwww: {score_name}={score_value}")
    #     #         self.langfuse.create_score(
    #     #             name=score_name,
    #     #             value=score_value,
    #     #             comment="Factually correct", # optional
    #     #         )
    #     #     print(f"[TracedOrchestrator] Método trace no disponible en Langfuse: {payload}")
    #     # except Exception as exc:
    #     #     print(f"[TracedOrchestrator] No se pudo enviar a Langfuse: {exc}")

    # def flush(self) -> None:
    #     """Fuerza el envío de todos los eventos pendientes a Langfuse."""
    #     if self._enabled and self.langfuse is not None:
    #         try:
    #             self.langfuse.flush()
    #             print("[TracedOrchestrator] Eventos enviados a Langfuse.")
    #         except Exception as e:
    #             print(f"[TracedOrchestrator] Error en flush: {e}")