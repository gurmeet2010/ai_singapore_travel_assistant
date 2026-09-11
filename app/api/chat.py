from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from app.agent.orchestrator import answer_question


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    message: str = Field(min_length=1, max_length=5000)


class ChatResponse(BaseModel):
    answer: str
    intent: list[str]
    routing_reason: str
    sources: list[dict[str, str]]
    tools_used: list[dict]


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        result = await answer_question(
            request.session_id,
            request.message,
        )
        return ChatResponse(**result)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="The travel assistant could not process the request.",
        ) from exc
