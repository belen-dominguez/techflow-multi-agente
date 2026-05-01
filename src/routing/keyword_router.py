
"""
keyword_router.py
-----------------
Responsabilidad: clasificar la intención de una consulta
usando un diccionario de palabras clave por dominio.


"""
from shared.logger import get_logger

log = get_logger("keyword_router")

KEYWORDS = {
        "hr": [
            "vacaciones", "vacacion", "licencia", "licencias",
            "salario", "sueldo", "bono", "aguinaldo", "remuneracion",
            "beneficio", "beneficios", "cobertura medica", "obra social",
            "prepaga", "capacitacion", "entrenamiento", "curso",
            "onboarding", "offboarding", "renuncia", "despido",
            "desvinculacion", "preaviso", "liquidacion",
            "evaluacion", "desempeño", "okr", "objetivo",
            "horario", "presencialidad", "home office", "remoto",
            "cumpleaños", "dia libre", "ausencia", "falta",
            "contrato", "periodo de prueba", "antigüedad",
            "gimnasio", "reembolso de gimnasio", "referido",
            "seguro de vida", "equipamiento", "laptop",
            "recursos humanos", "rrhh", "hr connect",
        ],
        "tech": [
            "soporte", "ticket", "incidente", "acceso", "accesos",
            "contraseña", "password", "vpn", "software", "sistema",
            "aplicacion", "app", "instalar", "instalacion",
            "computadora", "laptop", "equipo", "hardware",
            "red", "internet", "wifi", "correo", "email",
            "slack", "jira", "github", "confluence", "notion",
            "deploy", "deployment", "produccion", "staging",
            "bug", "error", "falla", "caido", "no funciona",
            "permiso", "permisos", "rol", "usuario",
            "2fa", "autenticacion", "seguridad", "firewall",
            "backup", "respaldo", "servidor", "cloud", "aws",
            "it support", "mesa de ayuda", "helpdesk",
            "datadog", "monitoreo", "alerta", "pagerduty",
            "pull request", "code review", "repositorio", "rama",
        ],
        "finance": [
            "gasto", "gastos", "reembolso", "reembolsar",
            "factura", "facturacion", "pago", "pagos", "contable",
            "presupuesto", "budget", "expensify",
            "tarjeta corporativa", "tarjeta de credito",
            "proveedor", "proveedores", "contrato de proveedor",
            "viaje", "viatico", "viaticos", "hotel", "vuelo",
            "comida de negocio", "almuerzo de equipo",
            "reporte financiero", "balance", "flujo de caja",
            "mrr", "arr", "churn", "cac", "ltv", "runway",
            "auditoria", "cierre contable", "centro de costo",
            "licencia de software", "suscripcion",
            "compra", "adquisicion", "cotizacion",
        ],
    }

class KeywordRouter:
    """
    Clasifica consultas por dominio usando coincidencia
    de palabras clave. No consume tokens de OpenAI.
    """

    def __init__(self, fallback_domain: str = "unknown"):
        """
        Args:
            fallback_domain: dominio a retornar si no hay coincidencias.
                             Por defecto "unknown".
        """
        self.fallback_domain = fallback_domain

    def route(self, query: str) -> str:
        """
        Clasifica una consulta en un dominio usando palabras clave.

        Estrategia: cuenta cuántas keywords de cada dominio aparecen
        en la query y elige el dominio con más coincidencias.
        Si hay empate o cero coincidencias, retorna el fallback.

        Args:
            query: consulta del usuario en texto libre.

        Returns:
            String con el dominio detectado: "hr", "tech" o "finance".
            Si no hay coincidencias, retorna el fallback_domain.
        """
        try:
            if not query or not query.strip():
                log.info(f"[KeywordRouter] Query vacía, usando fallback: "
                         f"'{self.fallback_domain}'")
                return self.fallback_domain

            query_normalized = query.lower().strip()

            scores = {}
            for domain, keywords in KEYWORDS.items():
                score = sum(
                    1 for keyword in keywords
                    if keyword in query_normalized
                )
                scores[domain] = score

            # best_domain = max(scores, key=lambda d: scores[d])
            # best_score = scores[best_domain]

            # if best_score == 0:
            #     log.info(f"[KeywordRouter] Sin coincidencias para '{query}'. "
            #              f"Usando fallback: '{self.fallback_domain}'")
            #     return self.fallback_domain

            # log.info(f"[KeywordRouter] Query: '{query}' -> "
            #          f"dominio: '{best_domain}' (score: {best_score})")
            best_score = max(scores.values())
            best_domains = [d for d, s in scores.items() if s == best_score]

            if best_score == 0 or len(best_domains) > 1:
                log.info(f"[KeywordRouter] Ambiguo o sin match para '{query}'. "
                        f"Usando fallback: '{self.fallback_domain}'")
                return self.fallback_domain

            best_domain = best_domains[0]
            return best_domain

        except Exception as e:
            log.error(f"[KeywordRouter] Error inesperado: {e}. "
                      f"Usando fallback: '{self.fallback_domain}'")
            return self.fallback_domain