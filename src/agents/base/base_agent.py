from typing import Any, Dict
from prompts.template import RAG_AGENT_PROMPT


class BaseRAGAgent:
    def __init__(self, retriever: Any, llm: Any, domain_name: str, logger):
        self.retriever = retriever
        self.llm = llm
        self.domain_name = domain_name
        self.log = logger

    def answer(self, question: str) -> Dict:
        try:
            chunks = self.retriever.retrieve(question)

            if not chunks:
                self.log.warning(f"[{self.domain_name}] Sin chunks para: '{question}'")
                return {
                    "response": "No encontré información relevante para responder esa consulta.",
                    "prompt": None
                }

            context = "\n\n".join(
                getattr(chunk, "page_content", str(chunk))
                for chunk in chunks
            )

            prompt = RAG_AGENT_PROMPT.format(
                domain=self.domain_name,
                context=context,
                question=question,
            )

            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, "content") else str(response)

            self.log.info(f"[{self.domain_name}], Respondiendo: '{content}'")

            return {
                "response": content,
                "prompt": prompt
            }
        except Exception as e:
            self.log.error(f"[{self.domain_name}] Error: {e}")

            return {
                "response": "Ocurrió un error al procesar la consulta.",
                "prompt": None
            }