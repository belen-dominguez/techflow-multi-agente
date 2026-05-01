"""
tracer.py
---------
Responsabilidad: instrumentar el flujo del sistema con Langfuse v4.

"""

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


        # no crea score pero lo deja en output.
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

