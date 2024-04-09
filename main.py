import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import uvicorn

from data_type import ChatData

open_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

async def chat(messages):
    client = OpenAI(api_key=open_api_key)
    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        temperature=0,
        stream=True  # again, we set stream=True
    )

    try:
        for chunk in response:
            content = chunk.choices[0].delta.content or f""
            yield content

    except Exception as e:
        print("OpenAI Response (Streaming) Error: " + str(e))
        raise HTTPException(503) 

@app.post("/api/chat/stream", response_class=StreamingResponse)
def run_agent_chat(input_data: ChatData):    
    return StreamingResponse(chat(input_data.messages))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))