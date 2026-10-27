from collections.abc import Callable
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.config import get_settings

LOADERS: dict[str, Callable[[Path], BaseLoader]] = {
	".pdf": lambda p: PyPDFLoader(str(p)),
	".txt": lambda p: TextLoader(str(p), encoding="utf-8"),
}


def file_loader(file_path: str | Path) -> list[Document]:
	"""Load a file based on its type and return its content as a list of documents."""
	path = Path(file_path)
	suffix = path.suffix.lower()

	factory = LOADERS.get(suffix)
	if factory is None:
		raise ValueError(f"Unsupported file type: {suffix or '(no extension)'}")

	try:
		return factory(path).load()
	except Exception as e:
		raise ValueError(f"Error loading {suffix} file: {path}") from e



def chunk_documents(doc):
	"""Chunk a list of documents into smaller pieces."""
	if not doc:
		return []
	try:
		splitter = RecursiveCharacterTextSplitter(
			chunk_size=get_settings().chunk_size,
			chunk_overlap=get_settings().chunk_overlap,
		)
		docs = splitter.split_documents(doc)
		if len(docs) == 0:
			raise ValueError("No chunks were created from the documents.")
		return docs
	except Exception as e:
		raise ValueError(f"Error chunking documents: {e}") from e
