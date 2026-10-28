from collections.abc import Callable
from pathlib import Path
import os
import tempfile
from pathlib import Path
from app.config import get_settings
from app.vector_store import get_vector_store

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import UploadFile
# from app.errors import IngestionError




READ_BLOCK_SIZE = 1024 * 1024


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
		docs = factory(path).load()
		if not docs:
			raise ValueError(f"No documents loaded from {path}.")
		return docs
	except Exception as e:
		raise ValueError(f"Error loading {suffix} file: {path}") from e


def chunk_documents(docs: list[Document]) -> list[Document]:
	"""Chunk a list of documents into smaller pieces."""
	if not docs:
		raise ValueError("No documents provided for chunking.")
	settings = get_settings()
	splitter = RecursiveCharacterTextSplitter(
		chunk_size=settings.chunk_size,
		chunk_overlap=settings.chunk_overlap,
	)
	docs = splitter.split_documents(docs)
	return docs


def build_chunk_ids(chunks: list[Document]) -> list[str]:
	"""Build unique IDs for each chunk."""
	if not chunks:
		raise ValueError("No chunks provided for building IDs.")

	ids: list[str] = []
	for i, chunk in enumerate(chunks):
		page = chunk.metadata.get("page", 0)
		source = chunk.metadata.get("source", "")
		id = f"{source}_page_{page}_{i}"
		ids.append(id)
	return ids


def add_documents_into_vector_store(chunks: list[Document]) -> Chroma:
	"""Embed a list of documents using Ollama embeddings."""
	if not chunks:
		raise ValueError("No chunks provided for embedding.")
	try:
		vector_store = get_vector_store()
		ids = build_chunk_ids(chunks)
		vector_store.delete(where={"source": chunks[0].metadata.get("source", "")})
		vector_store.add_documents(chunks, ids=ids)
		return vector_store
	except Exception as e:
		raise ValueError(f"Error embedding documents: {e}") from e


# async def upload_file(file) -> str:
# 	"""Save an uploaded file to the designated upload directory."""
# 	settings = get_settings()
# 	upload_dir = Path(settings.upload_dir)
# 	upload_dir.mkdir(parents=True, exist_ok=True)
# 	file_name: Path = file.filename.split("/")[-1].strip()
# 	if(not file_name):
# 		raise ValueError("Invalid file name.")
# 	suffix = file_name.suffix.lower()
# 	if suffix not in LOADERS:
# 		raise ValueError(f"Unsupported file type: {suffix or '(no extension)'}")
# 	file_path = upload_dir / file_name
# 	size = 0
# 	with file_path.open("wb") as buffer:
# 		while chunk := await file.read(1024 * 1024):
# 			size += len(chunk)
# 			if size > settings.max_file_size:
# 				buffer.close()
# 				file_path.unlink()
# 				raise ValueError("File size exceeds the maximum allowed size.")
# 			buffer.write(chunk)
# 	return str(file_path)




def _safe_file_name(raw_name: str | None) -> str:
	"""Keep only the base name of a client-provided file name."""
	if not raw_name:
		raise ValueError("Invalid file name.")
	name = Path(raw_name.replace("\\", "/")).name.strip()
	if not name:
		raise ValueError("Invalid file name.")
	return name


async def upload_file(file: UploadFile) -> Path:
	"""Save an uploaded file in the upload directory and return its path."""
	settings = get_settings()
	upload_dir = Path(settings.upload_dir).resolve()
	upload_dir.mkdir(parents=True, exist_ok=True)

	file_name = _safe_file_name(file.filename)
	suffix = Path(file_name).suffix.lower()
	if suffix not in LOADERS:
		raise ValueError(f"Unsupported file type: {suffix or '(no extension)'}")

	destination = (upload_dir / file_name).resolve()
	if not destination.is_relative_to(upload_dir):
		raise ValueError("Invalid file name.")

	fd, tmp_name = tempfile.mkstemp(dir=upload_dir, suffix=".part")
	tmp_path = Path(tmp_name)
	try:
		size = 0
		with os.fdopen(fd, "wb") as buffer:
			while block := await file.read(READ_BLOCK_SIZE):
				size += len(block)
				if size > settings.max_file_size:
					raise ValueError("File size exceeds the maximum allowed size.")
				buffer.write(block)
		tmp_path.replace(destination)
	finally:
		tmp_path.unlink(missing_ok=True)

	return destination

def exec_indexing(file_path: str | Path) -> Chroma:
	"""Load, chunk, and embed documents from a file."""
	output = file_loader(file_path)
	chunks = chunk_documents(output)
	embedded = add_documents_into_vector_store(chunks)
	return embedded
