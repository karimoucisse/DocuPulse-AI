from fastapi import FastAPI, File, Form
from fastapi.middleware.cors import CORSMiddleware
from app.config import 	get_settings


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
@app.post('/upload')
def upload( file: bytes = File(...)):
	return {"message": f"File added: {file} uploaded successfully"}
