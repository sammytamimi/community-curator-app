import os
from openai import AzureOpenAI
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01",
)


class ChatMessage(BaseModel):
    message: str


@router.post("/chat")
async def chat(message: ChatMessage):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message.message},
        ],
    )
    return {"response": response.choices[0].message.content}
