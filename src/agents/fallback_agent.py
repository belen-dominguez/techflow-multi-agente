from shared.logger import get_logger

log = get_logger("fallback_agent")

class FallbackAgent:
    def answer(self, question: str):
        respuesta = ("Lo siento, no tengo información específica sobre ese tema. "
                    "¿Podrías proporcionar más detalles o hacer una pregunta diferente?")
        log.info(f"[FallbackAgent] Respondiendo: '{respuesta}'")
        
        return {
            "response": respuesta,
            "prompt": None,
            "confidence": "low"
        }