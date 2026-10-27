from collections.abc import Callable
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
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

def chunk_documents(docs: list[Document]) -> list[Document]:
	"""Chunk a list of documents into smaller pieces."""
	if not docs:
		return []
	try:
		splitter = RecursiveCharacterTextSplitter(
			chunk_size=get_settings().chunk_size,
			chunk_overlap=get_settings().chunk_overlap,
		)
		docs = splitter.split_documents(docs)
		return docs
	except Exception as e:
		raise ValueError(f"Error chunking documents: {e}") from e

def build_chunk_ids(chunks: list[Document]) -> list[str]:
	"""Chunk a list of documents into smaller pieces and return their IDs."""
	if not chunks:
		return []
	try:
		ids: list[str] = []
		for i, chunk in enumerate(chunks):
			page = chunk.metadata.get("page", 0)
			source = chunk.metadata.get("source", "")
			chunk.metadata["id"] = f"{source}_page_{page}_{i}"
			ids.append(chunk.metadata["id"])
		return ids
	except Exception as e:
		raise ValueError(f"Error chunking document IDs: {e}") from e

def vectorize_documents(chunks: list[Document]) -> Chroma | None:
	"""Embed a list of documents using Ollama embeddings."""
	if not chunks:
		return []
	try:
		embeddings = OllamaEmbeddings(model=get_settings().embedding_model)
		vector_store = Chroma(
			collection_name=get_settings().vector_store_name,
			persist_directory=get_settings().vector_store_path,
			embedding_function=embeddings
		)
		if not vector_store:
			raise ValueError("Failed to create vector store.")
		ids = build_chunk_ids(chunks)
		vector_store.delete(where={"id": {"$in": ids}})
		vector_store.add_documents(chunks, ids=ids)
		return vector_store
	except Exception as e:
		raise ValueError(f"Error embedding documents: {e}") from e
