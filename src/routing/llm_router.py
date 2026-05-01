"""
llm_router.py
-------------
Responsabilidad: clasificar la intención de una consulta
usando un LLM para entender el significado semántico,
no solo palabras clave.

"""

from typing import Any
from shared.logger import get_logger
from prompts.template import LLM_ROUTER_PROMPT


log = get_logger("LLMRouter")

class LLMRouter:
    """
    Clasifica consultas por dominio usando un LLM.
    Más robusto que KeywordRouter pero consume tokens.
    """

    # Dominios válidos que puede retornar el LLM
    VALID_DOMAINS = {"hr", "tech", "finance"}

    def __init__(self, llm: Any, fallback_domain: str = "unknown"):
        """
        Args:
            llm:             modelo de lenguaje de LangChain (ej: ChatOpenAI).
                             Debe estar configurado con temperatura baja
                             para respuestas más deterministas.
            fallback_domain: dominio a retornar si el LLM no responde
                             con un valor válido.
        """
        self.llm = llm
        self.fallback_domain = fallback_domain

    def route(self, query: str) -> str:
        """
        Clasifica una consulta en un dominio usando el LLM.

        Le pide al LLM que responda ÚNICAMENTE con una palabra:
        "hr", "tech", "finance" o "unknown".
        Si la respuesta no es válida, usa el fallback.

        Args:
            query: consulta del usuario en texto libre.

        Returns:
            String con el dominio detectado: "hr", "tech" o "finance".
            Si el LLM responde "unknown" o algo inválido, retorna fallback_domain.
        """
        try:
            if not query or not query.strip():
                log.info(f"[LLMRouter] Query vacía, usando fallback: "
                         f"'{self.fallback_domain}'")
                return self.fallback_domain

            # Armamos el prompt de clasificación
            prompt = LLM_ROUTER_PROMPT.format(question=query)

            # Llamamos al LLM
            response = self.llm.invoke(prompt)

            # Parseamos y normalizamos la respuesta
            domain = self._parse_response(response.content)

            log.info(f"[LLMRouter] Query: '{query}' -> dominio: '{domain}'")
            return domain

        except Exception as e:
            log.error(f"[LLMRouter] Error al clasificar query: {e}. "
                      f"Usando fallback: '{self.fallback_domain}'")
            return self.fallback_domain

    def _parse_response(self, response_text: str) -> str:
        """
        Parsea la respuesta del LLM y la valida.

        El LLM a veces agrega espacios, puntuación o texto extra.
        Esta función lo limpia y verifica que sea un dominio válido.

        Args:
            response_text: texto crudo devuelto por el LLM.

        Returns:
            Dominio válido ("hr", "tech" o "finance"),
            o fallback_domain si la respuesta no es válida.
        """
        # Limpiamos la respuesta
        cleaned = response_text.strip().lower()

        for char in [".", ",", ":", "\"", "'"]:
            cleaned = cleaned.replace(char, "")

        # Tomamos solo la primera palabra por si el LLM agregó explicación
        first_word = cleaned.split()[0] if cleaned.split() else ""

        if first_word in self.VALID_DOMAINS:
            return first_word

        if first_word == "unknown":
            log.info(f"[LLMRouter] El LLM respondió 'unknown'. "
                      f"Usando fallback: '{self.fallback_domain}'")
            return self.fallback_domain

        log.info(f"[LLMRouter] Respuesta inesperada del LLM: '{response_text}'. "
                  f"Usando fallback: '{self.fallback_domain}'")
        return self.fallback_domain