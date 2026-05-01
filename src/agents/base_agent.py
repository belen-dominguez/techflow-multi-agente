from typing import Any, Dict
from prompts.template import RAG_AGENT_PROMPT


class BaseRAGAgent:
    def __init__(self, retriever: Any, llm: Any, domain_name: str, logger):
        self.retriever = retriever
        self.llm = llm
        self.domain_name = domain_name
        self.log = logger

    def answer(self, question: str) -> Dict:
        chunks = self.retriever.retrieve(question)

        context = "\n\n".join(chunk.page_content for chunk in chunks)

        prompt = RAG_AGENT_PROMPT.format(
            domain=self.domain_name,
            context=context,
            question=question,
        )

        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, "content") else str(response)

        self.log.info(f"[{self.domain_name}] Respondiendo: '{content}'")

        return {
            "response": content,
            "prompt": prompt
        }