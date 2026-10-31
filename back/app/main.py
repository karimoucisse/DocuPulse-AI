from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.ingestion import ingest_file, upload_file
from app.rag import answer_question
from app.schemas import ChatResponse

app = FastAPI()
settings = get_settings()
origins = settings.cors_origins
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.post("/upload")
async def upload(file: UploadFile = File):
	file_path = await upload_file(file)
	count = await ingest_file(file_path)
	return {f"filename: {file.filename} chunks: {count}"}


@app.post("/question")
def getResponse(body: dict[str, str]):
	res: ChatResponse = answer_question(body["question"])
	return res
