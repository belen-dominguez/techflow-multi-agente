"""
orchestrator.py
---------------
Responsabilidad: recibir la consulta del usuario, clasificar
su intención usando el router, y delegarla al agente correcto.

"""
from typing import Any,  Dict
from shared.config_loader import ConfigLoader
from shared.logger import get_logger

config = ConfigLoader()
log = get_logger("orchestrator")

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
        self.fallback_domain = config.get("routing.fallback_domain", "unknown")

    def route(self, question: str) -> dict:
        """Clasifica la consulta y la envía al agente adecuado."""
       
        if not question or not question.strip():
                raise ValueError("La consulta no puede estar vacía.")
              

        with self.tracer.start_span("orchestrator"):

            # Paso 1: detectar el dominio
            domain = self.router.route(question)

            # 2. Normalización + fallback
            domain = domain if domain in self.agents else self.fallback_domain

            # 3. Validación fuerte (config error)
            if domain not in self.agents:
                raise RuntimeError(
                    f"No hay agente fallback configurado: '{domain}'"
            )

            
            self.tracer.set_output({
                "selected_agent": domain
            })

    
            log.info(f"[Orchestrator] Enrutando a agente '{domain}'...")

            with self.tracer.start_span(domain):
                # Paso 4: delegar al agente
                try:
                    result = self.agents[domain].answer(question)
                except Exception as e:
                    log.error(f"[Orchestrator] Error en agente '{domain}': {e}")

                    domain = self.fallback_domain
                    result = self.agents[domain].answer(question)
                
    
                self.tracer.set_output({
                    "prompt": result.get("prompt", None),
                    "response": result.get("response", "")
                })

                result["routed_by"] = self.router.__class__.__name__
       
                return {
                    "domain": domain,
                    "answer": result.get("response", ""),
                    "prompt": result.get("prompt"),
                    "routed_by":  self.router.__class__.__name__
                }

