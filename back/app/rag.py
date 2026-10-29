from textwrap import dedent

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_ollama import ChatOllama
from app.schemas import Source, ChatResponse
from app.config import get_settings
from app.vector_store import get_vector_store
from functools import lru_cache

QUOTE_MAX_LENGTH = 200
PERTINENCE = 0.9

def retrieve_relevant_chunks(query: str) -> tuple[Document, float]:
	"""Retrieve documents from the vector store based on a query."""
	try:
		vector_store = get_vector_store()
		return vector_store.similarity_search_with_score(query, k=get_settings().top_k)
	except Exception as e:
		raise ValueError(f"Error retrieving documents: {e}") from e


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
		if source:
			sources.append(source)
	return sources

PROMPT = ChatPromptTemplate.from_template(
	dedent(
		"""
		Answer the question based only on the following context
		and respond from the same language as the question:

		Context:
		{context}

		The question is delimited by << and >> :

		Question = "" {question} ""

		Answer:

		If the answer is not contained within the context, say "I don't know".
		"""
	)
)

@lru_cache
def get_chat_model() -> ChatOllama:
	settings = get_settings()
	return ChatOllama(
		model=settings.chat_model,
		temperature=settings.temperature,
	)

def generate_response(query: str, chunks: list[Document]) -> str:
	chat = get_chat_model()
	context = format_docs(chunks)
	rag_chain = (
		{
			"context": lambda _: context,
			"question": RunnablePassthrough(),
		}
		| PROMPT
		| chat
		| StrOutputParser()
	)

	return rag_chain.invoke(query)

def filter_chunks_by_score(docs: list[Document, float]) -> list[Document, float] | None:
	return [doc for doc, score in docs if score <= PERTINENCE ]



def answer_question(query: str) -> ChatResponse:
	docs = retrieve_relevant_chunks(query)
	chunks = filter_chunks_by_score(docs)
	if not chunks:
		raise ValueError("No relevant documents found for the query.")
	sources = build_sources(chunks)
	response = generate_response(query, chunks)
	print(response)
	return {"answer": response, "sources": sources}

