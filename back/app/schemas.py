from pydantic import BaseModel, ConfigDict, Field

REQUEST_MAX_LENGTH = 1000


class Source(BaseModel):
	"""A source of information for the RAG system."""

	source: str = Field(description="The name of the source file.")
	page: int | None = Field(
		default=None,
		ge=1,
		description="The page number in the source file. Can be None if not applicable.",
	)
	quote: str = Field(description="The quote extracted from the source file.")


class UserQuestion(BaseModel):
	"""A question from the user to the RAG system."""

	model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
	query: str = Field(
		min_length=1,
		description="The user's query for the RAG system.",
		max_length=REQUEST_MAX_LENGTH,
	)


class ChatResponse(BaseModel):
	"""A response from the RAG system to the user."""

	model_config = ConfigDict(extra="forbid")
	answer: str = Field(description="The generated answer from the RAG system.", min_length=1)
	sources: list[Source] = Field(description="List of sources used to generate the answer.")


class UploadResponse(BaseModel):
	"""Represents an uploaded file with its metadata."""

	model_config = ConfigDict(extra="forbid")
	file_name: str = Field(description="The name of the uploaded file.")
	chunks_count: int | None = Field(
		default=None, ge=1, description="The number of chunks in the uploaded file."
	)
