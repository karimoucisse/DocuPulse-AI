# from pathlib import Path
# from typing import Annotated, Literal
# from xml.dom.minidom import Document
# from langchain_community.document_loaders import TextLoader, PyPDFLoader
# from langchain_core.documents import Document


# def exe_loader(file_path: Path, file_type: str, func: callable) -> list[Document]:
# 	try:
# 		loader = func(file_path, encoding="utf-8" if file_type == "txt" else "")
# 		return loader.load()
# 	except Exception as e:
# 		raise ValueError(f"Error loading {file_type} file: {file_path}") from e

# file_type_loader: dict[str, callable] = {
# 	"pdf": PyPDFLoader,
# 	"txt": TextLoader
# }

# def file_loader(file_path: Path) -> list[Document]:
# 	"""Load a file based on its type and return its content as a list of documents."""
# 	file_type = file_path.split(".")[-1].lower()
# 	if file_type not in file_type_loader:
# 		raise ValueError(f"Unsupported file type: {file_type}")
# 	loader = file_type_loader.get(file_type)
# 	if not loader:
# 		raise ValueError(f"Unsupported file type: {file_type}")
# 	return exe_loader(file_path, file_type, loader)


from collections.abc import Callable
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

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
