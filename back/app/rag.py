from app.config import get_settings
from app.vector_store import get_vector_store
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.documents import Document

def retrieve_documents(query: str) -> list[Document]:
	"""Retrieve documents from the vector store based on a query."""
	try:
		vector_store = get_vector_store()
		results = vector_store.similarity_search(query, k=get_settings().top_k)
		return results
	except Exception as e:
		raise ValueError(f"Error retrieving documents: {e}") from e

def generate_response(query: str, retrieved_docs: list[Document]) -> str:
	# llm => chat + modele
	# prompt
	
