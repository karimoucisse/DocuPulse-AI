from functools import lru_cache
from textwrap import dedent

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.runnables import Runnable
from app.config import get_settings
from app.schemas import ChatResponse, Source
from app.vector_store import get_vector_store

QUOTE_MAX_LENGTH = 200
PERTINENCE = 0.75


def filter_chunks_by_score(docs: list[Document, float]) -> list[Document]:
	if not docs or min([score for doc, score in docs]) > PERTINENCE:
		return []
	return [doc for doc, score in docs]


def retrieve_relevant_chunks(query: str) -> list[Document]:
	"""Retrieve documents from the vector store based on a query."""
	vector_store = get_vector_store()
	docs = vector_store.similarity_search_with_score(query, k=get_settings().top_k)
	return filter_chunks_by_score(docs)


def format_docs(docs: list[Document]) -> str:
	return "\n\n".join(doc.page_content for doc in docs)


def build_sources(docs: list[Document]) -> list[Source]:
	"""Build a string of sources from the documents."""
	if not docs:
		raise ValueError("No documents provided for building sources.")
	sources = []
	for doc in docs:
		data = doc.metadata
		data["quote"] = doc.page_content[:QUOTE_MAX_LENGTH]
		source = Source(**data)
		sources.append(source)
	return sources


PROMPT = ChatPromptTemplate.from_template(
	dedent(
		"""

		Answer the question based only on the following context
		and nothing else, respond from the same language as the question:
		The question and the context are delimited by <<< and >>> :

		Context: <<< {context} >>>


		Question: <<< {question} >>>

		If the answer is not contained within the context,
		say that you don't know in the proper language.

		Answer:

		"""
	)
)


@lru_cache
def get_chat_model() -> ChatOllama:
	settings = get_settings()
	return ChatOllama(
		model=settings.chat_model, temperature=settings.temperature, base_url=settings.ollama_url
	)

@lru_cache
def get_rag_chain() -> Runnable:
	chat = get_chat_model()
	rag_chain = PROMPT | chat | StrOutputParser()
	return rag_chain


def answer_question(query: str) -> ChatResponse:
	chunks = retrieve_relevant_chunks(query)
	if not chunks:
		return ChatResponse(answer="No relevant documents found for the query.", sources=[])
	sources = build_sources(chunks)
	context = format_docs(chunks)
	chain = get_rag_chain()
	response = chain.invoke({"context": context, "question": query})
	return ChatResponse(answer=response, sources=sources)
