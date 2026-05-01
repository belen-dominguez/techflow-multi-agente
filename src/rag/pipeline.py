
from typing import  Optional

from langchain.embeddings.base import Embeddings
from langchain_core.documents import Document

from rag.chunker import Chunker
from rag.embeddings import EmbeddingStore
from rag.loader import DocumentLoader
from rag.retriver import Retriever
from shared.config_loader import ConfigLoader


class RAGPipeline:
    """Construye el pipeline RAG completo para un dominio."""

    def __init__(self, domain: str, config: ConfigLoader):
        """Inicializa el pipeline para un dominio específico.

        Args:
            domain: nombre del dominio ("hr", "tech", "finance").
            config: instancia de ConfigLoader con la configuración.
        """
        self.domain = domain
        self.config = config
        self.retriever: Optional[Retriever] = None

    def build(self, embeddings: Embeddings) -> Retriever:
        """Construye y retorna el retriever RAG listo para usar.

        Pasos internos:
          1. Carga los documentos del dominio
          2. Los divide en chunks
          3. Genera embeddings y los guarda en FAISS
          4. Crea y retorna el retriever

        Args:
            embeddings: modelo de embeddings de LangChain.

        Returns:
            Instancia de Retriever lista para hacer búsquedas.
        """
        try:
            print(f"[RAGPipeline] Construyendo retriever para '{self.domain}'...")

            # Paso 1: cargar documentos del dominio
            data_path = self.config.get(f"documents.{self.domain}_path")
            loader = DocumentLoader(folder_path=data_path)
            documents = loader.load()
            print(f"✅ {len(documents)} documentos cargados")

            # Paso 2: dividir en chunks
            chunker = Chunker(
                chunk_size=self.config.get("chunking.chunk_size"),
                chunk_overlap=self.config.get("chunking.chunk_overlap"), 
            )
            chunks = chunker.chunk_documents(documents)
            print(f"✅ {len(chunks)} chunks creados")

            # Paso 3: generar embeddings y guardar en FAISS
            index_path = self.config.get("vector_store.persist_directory") + f"/{self.domain}"
            store = EmbeddingStore(embeddings=embeddings, index_path=index_path)
            store.build_and_save(chunks)
            print(f"✅ Índice construido y guardado en {index_path}")

            # Paso 4: crear y retornar el retriever
            self.retriever = Retriever(store.index)
            return self.retriever

        except Exception as error:
            raise RuntimeError(
                f"Error al construir el pipeline para '{self.domain}': {error}"
            ) from error

    def retrieve(self, query: str, k: int = 4) -> list[tuple]:
        """Busca documentos relevantes para una query.

        Args:
            query: pregunta o búsqueda de texto.
            k: número de documentos a retornar.

        Returns:
            Lista de tuplas (Document, puntuación_similitud).
        """
        if self.retriever is None:
            raise ValueError("El pipeline no ha sido construido. Llama build() primero.")

        return self.retriever.retrieve_with_scores(query, k=k)
