
from typing import Annotated, Literal
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from app.indexing.chunk import chunk_documents

SOURCE = Annotated[str,  Literal["pdf", "txt"]]

def pdf_loader(file_path: str):
	"""Load a PDF file and return its content as a list of documents."""
	try:
		loader = PyPDFLoader(file_path)
		doc = loader.load()
		return doc
	except Exception as e:
		raise ValueError(f"Error loading PDF file: {file_path}") from e

def txt_loader(file_path: str):
	"""Load a text file and return its content as a list of documents."""
	try:
		loader = TextLoader(file_path)
		doc = loader.load()
		return doc
	except Exception as e:
		raise ValueError(f"Error loading text file: {file_path}") from e

define_loader = {
	"pdf": pdf_loader,
	"txt": txt_loader
}

def file_loader(file_path: str):
	"""Load a file based on its type and return its content as a list of documents."""
	file_type = pathlib
	loader = define_loader.get(file_type)
	if not loader:
		raise ValueError(f"Unsupported file type: {file_type}")
	return loader(file_path)

file_path = "data/sample.pdf"
file_type = "pdf"
output = file_loader(file_path, file_type)
chunks = chunk_documents(output)
print(f"Chunked into {len(chunks)} chunks.")
