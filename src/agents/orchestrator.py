"""
orchestrator.py
---------------
Responsabilidad: recibir la consulta del usuario, clasificar
su intención usando el router, y delegarla al agente correcto.

Uso:
    from agents.orchestrator import Orchestrator

    orchestrator = Orchestrator(
        router=router,
        agents={"hr": hr_agent, "tech": tech_agent, "finance": finance_agent},
    )
    result = orchestrator.route("¿Cuántos días de vacaciones tengo?")
"""
from typing import Any, Callable, Dict
import uuid

from shared import tracer

class Orchestrator:
    """Clasifica la consulta del usuario y la delega al agente especializado correspondiente."""

    def __init__(
        self,
        router: Any,
        agents: Dict[str, Any],
        tracer: Any,
    ):
        """Inicializa el Orchestrator con el router y los agentes.

        Args:
            router: componente responsable de decidir el dominio.
            agents: diccionario de agentes por dominio.
            tracer: componente responsable de rastrear la ejecución.
        """
        self.router = router
        self.agents = agents
        self.tracer = tracer

    def route(self, question: str) -> dict:
        # """Clasifica la consulta y la envía al agente adecuado."""
        # domain = self.router.route(question)

        # if domain not in self.agents:
        #     raise ValueError(f"Dominio '{domain}' no tiene agente asignado.")

        # agent = self.agents[domain]
        # answer = agent.answer(question)
        # return {"domain": domain, "answer": answer, "routed_by": self.router.__class__.__name__}

        if not question or not question.strip():
                raise ValueError("La consulta no puede estar vacía.")
        
         

        with self.tracer.start_span("orchestrator"):

            # Paso 1: detectar el dominio
            domain = self.router.route(question)

            # Paso 2: si el dominio no tiene agente, usamos el fallback
            if domain not in self.agents:
                print(f"[Orchestrator] Dominio '{domain}' sin agente. "
                        f"Usando fallback: 'hr'")
                domain = "hr"

            
            self.tracer.set_output({
                "selected_agent": domain
            })

            # Paso 3: delegar al agente
            print(f"[Orchestrator] Enrutando a agente '{domain}'...")

            with self.tracer.start_span(domain):

                result = self.agents[domain].answer(question)
                
                self.tracer.set_output({"prompt": result["prompt"], "response": result["response"]})

                result["routed_by"] = self.router.__class__.__name__

                return {
                    "domain": domain,
                    "answer":result["response"],
                    "prompt":  result["prompt"],
                    "routed_by": "keyword_router"              
                }        


    def add_agent(self, domain: str, agent: Any) -> None:
        """Agrega o reemplaza un agente para un dominio específico."""
        self.agents[domain] = agent

    def get_agent(self, domain: str) -> Any:
        """Retorna el agente asignado a un dominio."""
        return self.agents.get(domain)
