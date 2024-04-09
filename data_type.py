from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str


class ChatData(BaseModel):
    messages: list[Message] = []
    prompt: str = None
