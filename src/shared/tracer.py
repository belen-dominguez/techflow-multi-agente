"""
tracer.py
---------
Responsabilidad: instrumentar el flujo del sistema con Langfuse v4.

"""

from dotenv import load_dotenv

from langfuse import Langfuse


load_dotenv()


class _DummyContext:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    @property
    def id(self):
        return "no-trace"

class Tracer:
    def __init__(self):
        try:
            self.client = Langfuse()
        except Exception as e:
            print(f"[Tracer] Error inicializando Langfuse: {e}")
            self.client = None

    def _safe(self, fn, *args, default=None, **kwargs):
        if not self.client:
            return default

        try:
            return fn(*args, **kwargs)
        except Exception as e:
            print(f"[Tracer] Error: {e}")
            return default

    # iniciar trace
    def start_trace(self, name: str,  input_data: dict):
         return self._safe(
            self.client.start_as_current_observation,
            name=name,
            input=input_data,
            default=_DummyContext()
        )
    

    # crear span
    def start_span(self, name: str, input_data: dict = None):
        return self._safe(
            self.client.start_as_current_observation,
            name=name,
            input=input_data,
            default=_DummyContext()
        )
    
    # guardar output final
    def set_output(self, output_data: dict):
        self._safe(
            self.client.update_current_span,
            output=output_data
        )


      
    # guardar scores
    def add_score(self,trace_id: str, name: str, value: float, comment: str = None):
        self._safe(
        self.client.create_score,
        trace_id=trace_id,
        name=name,
        value=value,
        comment=comment,
    )

  
        self._safe(
            self.client.update_current_span,
            output={
                "score_name": name,
                "score_value": value,
                "score_comment": comment
            }
        )

      
    # fuerza el envío inmediato de todo
    def flush(self):
          self._safe(self.client.flush)

