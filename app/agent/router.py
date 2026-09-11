from typing import Literal

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from app.agent.prompts import ROUTER_PROMPT
from app.config import get_settings


class RouteDecision(BaseModel):
    sources: list[
        Literal["RAG", "WEATHER_MCP", "CURRENCY_MCP"]
    ] = Field(min_length=1)

    reason: str


def get_router():

    settings = get_settings()

    model = ChatGoogleGenerativeAI(
        model=settings.gemini_chat_model,
        temperature=0,
        google_api_key=settings.gemini_api_key,
         max_retries=1,
    )

    return ROUTER_PROMPT | model.with_structured_output(RouteDecision)


async def route_question(question: str) -> RouteDecision:

    chain = get_router()

    return await chain.ainvoke(
        {"question": question}
    )