from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from shared.logger import get_logger

log = get_logger("chunker")

class Chunker:
    """Divide Documents en fragmentos usando RecursiveCharacterTextSplitter."""

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 100,
        separators: List[str] | None = None,
    ):
        """Inicializa el Chunker con el tamaño y solapamiento deseado."""
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ".", " "]

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """Convierte una lista de Documents en una lista de Documents más pequeños."""

        try:
            if not documents:
                raise ValueError(
                    "La lista de documentos está vacía. "
                    "Verificá que el DocumentLoader haya cargado archivos."
                )
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                separators=self.separators,
            )

            chunked_documents: List[Document] = []

            for original in documents:
                # Divide el texto del documento original en varios fragmentos.
                chunks = splitter.split_text(original.page_content)

                for index, chunk_text in enumerate(chunks, start=1):
                    # Cada chunk conserva metadata del documento original.
                    chunked_documents.append(
                        Document(
                            page_content=chunk_text,
                            metadata={
                                **original.metadata,
                                "chunk_index": index,
                                "chunk_source": original.metadata.get("source", "unknown"),
                            },
                        )
                    )

            return chunked_documents
        except ValueError:
                    raise
        except Exception as e:
            raise RuntimeError(f"Error inesperado al dividir documentos: {e}")

def chunk_documents(
    documents: List[Document],
    chunk_size: int = 500,
    chunk_overlap: int = 100,
) -> List[Document]:
    """Función de conveniencia para dividir Documents sin instanciar la clase."""
    chunker = Chunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return chunker.chunk_documents(documents)
