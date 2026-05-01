from pathlib import Path
from typing import List

from langchain_core.documents import Document
from shared.logger import get_logger

log = get_logger("DocumentLoader")

class DocumentLoader:
    """Carga archivos de texto desde una carpeta y los convierte en Document de LangChain."""

    def __init__(self, folder_path: str):
        """Inicializa el cargador con la ruta de la carpeta."""
        self.folder_path = Path(folder_path)

    def load(self) -> List[Document]:
        """Carga todos los archivos .txt y .md y devuelve una lista de Document."""
        if not self.folder_path.exists():
            raise FileNotFoundError(f'La carpeta no existe: {self.folder_path}')
        if not self.folder_path.is_dir():
            raise NotADirectoryError(f'No es una carpeta válida: {self.folder_path}')

        documents: List[Document] = []

        for file_path in sorted(self.folder_path.glob('*')):
            if file_path.suffix.lower() not in {'.txt', '.md'}:
                continue

            text = file_path.read_text(encoding='utf-8')

            document = Document(
                page_content=text,
                metadata={
                    'source': str(file_path),
                    'name': file_path.name,
                },
            )
            documents.append(document)

        return documents


def load_documents_from_folder(folder_path: str) -> List[Document]:
    """Función de conveniencia para cargar documentos sin instanciar la clase."""
    loader = DocumentLoader(folder_path)
    return loader.load()
