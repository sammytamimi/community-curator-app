import os
import json
from openai import AzureOpenAI
from pydantic import BaseModel
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

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


@router.post("/chat/stream")
async def chat_stream(message: ChatMessage):
    def generate():
        try:
            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_DEPLOYMENT_ID"),
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": message.message},
                ],
                stream=True,
            )
            
            for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta.content is not None:
                        data = {
                            "content": delta.content,
                            "done": False
                        }
                        yield f"data: {json.dumps(data)}\n\n"
            
            # Send done signal
            yield f"data: {json.dumps({'content': '', 'done': True})}\n\n"
            
        except Exception as e:
            error_data = {
                "error": str(e),
                "done": True
            }
            yield f"data: {json.dumps(error_data)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type",
        }
    )



