from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from app.config import get_settings


def get_vector_store() -> Chroma:
	"""Get the vector store."""
	settings = get_settings()
	embeddings = OllamaEmbeddings(model=settings.embedding_model)
	vector_store = Chroma(
		collection_name=settings.vector_store_name,
		persist_directory=settings.vector_store_path,
		embedding_function=embeddings,
	)
	return vector_store
