from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import get_settings


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
