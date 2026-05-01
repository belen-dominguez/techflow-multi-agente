from typing import List

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS


class Retriever:
    """Ejecuta búsquedas semánticas en el vector store y devuelve chunks relevantes."""

    def __init__(self, faiss_index: FAISS):
        """Inicializa el Retriever con un índice FAISS ya construido.

        1. Esta función se ejecuta primero cuando creas el objeto Retriever.
        """
        self.index = faiss_index

    def retrieve(self, query: str, k: int = 4) -> List[Document]:
        """Busca los k documentos más relevantes para una query.

        Se ejecuta cuando tienes una pregunta y quieres encontrar chunks relacionados.
        """
        try:
            # Realiza una búsqueda de similitud semántica en el índice FAISS.
            documents = self.index.similarity_search(query, k=k)
            return documents
        except Exception as error:
            raise RuntimeError("Error durante la búsqueda de similitud") from error

    def retrieve_with_scores(self, query: str, k: int = 4) -> List[tuple]:
        """Busca documentos con sus puntuaciones de similitud.

        Se utiliza cuando necesitas saber qué tan relevante es cada resultado.
        """
        try:
            # Realiza búsqueda y devuelve documentos con score de similitud.
            results = self.index.similarity_search_with_relevance_scores(query, k=k)
            return results
        except Exception as error:
            raise RuntimeError("Error durante la búsqueda con puntuaciones") from error


def create_retriever(faiss_index: FAISS) -> Retriever:
    """Función de conveniencia para crear una instancia de Retriever."""
    return Retriever(faiss_index=faiss_index)
