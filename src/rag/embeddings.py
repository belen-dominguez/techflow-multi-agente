from pathlib import Path
from typing import List, Optional

from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from shared.logger import get_logger

log = get_logger("rag.embeddings")

class EmbeddingStore:
    """Genera embeddings para una lista de chunks y los guarda en FAISS."""

    def __init__(self, embeddings: Embeddings, index_path: str):
        """Inicializa el almacén de embeddings y la ruta de persistencia.

        1. Esta función se ejecuta primero cuando creas el objeto EmbeddingStore.
        """
        self.embeddings = embeddings
        self.index_path = Path(index_path)
        self.index: Optional[FAISS] = None

        # Asegura que la carpeta del índice exista antes de guardar.
        self.index_path.mkdir(parents=True, exist_ok=True)

    def build_index(self, chunks: List[Document]) -> FAISS:
        """Construye un índice FAISS a partir de una lista de chunks.

        Se ejecuta después de crear la instancia y antes de guardar el índice.
        Esta función maneja errores de generación de embeddings.
        """
        try:
            self.index = FAISS.from_documents(chunks, self.embeddings)
            log.info(f"[EmbeddingStore] ✅ Índice construido para {len(chunks)} chunks")
            return self.index
        except Exception as error:
            raise RuntimeError("Error creando el índice FAISS desde los chunks") from error

    def save_index(self) -> None:
        """Guarda el índice FAISS en disco en la carpeta especificada.

        Se ejecuta después de build_index() y requiere que el índice ya exista.
        Esta función maneja errores de persistencia en disco.
        """
        if self.index is None:
            raise ValueError("El índice no ha sido construido todavía.")

        try:
            self.index.save_local(str(self.index_path))
            log.info(f"[EmbeddingStore] ✅ Índice guardado en {self.index_path}")
        except Exception as error:
            raise RuntimeError("Error guardando el índice FAISS en disco") from error

    def load_index(self) -> FAISS:
        """Carga un índice FAISS existente desde disco.

        Se utiliza cuando ya existe un índice guardado y quieres reutilizarlo.
        """
        self.index = FAISS.load_local(str(self.index_path), self.embeddings)
        log.info(f"[EmbeddingStore] ✅ Índice cargado desde {self.index_path}")
        return self.index

    def build_and_save(self, chunks: List[Document]) -> FAISS:
        """Construye el índice desde los chunks y lo guarda en disco.

        """
        self.build_index(chunks)
        self.save_index()
        return self.index


def create_embedding_store(embeddings: Embeddings, index_path: str) -> EmbeddingStore:
    """Función de conveniencia para crear una instancia de EmbeddingStore.

    """
    return EmbeddingStore(embeddings=embeddings, index_path=index_path)
