from textwrap import dedent

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_ollama import ChatOllama

from app.config import get_settings
from app.vector_store import get_vector_store


def retrieve_documents(query: str) -> list[Document]:
	"""Retrieve documents from the vector store based on a query."""
	try:
		vector_store = get_vector_store()
		return vector_store.similarity_search(query, k=get_settings().top_k)
	except Exception as e:
		raise ValueError(f"Error retrieving documents: {e}") from e


def format_docs(docs: list[Document]) -> str:
	return "\n\n".join(doc.page_content for doc in docs)


PROMPT = ChatPromptTemplate.from_template(
	dedent(
		"""
		Answer the question based only on the following context:

		Context:
		{context}

		The question is delimited by <<< and >>>:

		Question = <<< {question} >>>

		Answer concisely. If the context does not contain the answer,
		say "I don't know".
		"""
	)
)


def generate_response(query: str) -> str:
	settings = get_settings()

	chat = ChatOllama(
		model=settings.chat_model,
		temperature=settings.temperature,
	)

	rag_chain = (
		{
			"context": RunnableLambda(retrieve_documents) | format_docs,
			"question": RunnablePassthrough(),
		}
		| PROMPT
		| chat
		| StrOutputParser()
	)

	return rag_chain.invoke(query)
