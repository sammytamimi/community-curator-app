import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
)


class ChatMessage(BaseModel):
    message: str


@app.post("/chat")
async def chat(message: ChatMessage):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.message},
        ],
    )
    return {"response": response.choices[0].message.content}


@app.get("/")
async def root():
    return {"message": "Hello World"}