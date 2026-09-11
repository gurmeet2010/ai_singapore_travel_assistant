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


def _create_router():
    """
    Create the router chain once.

    The chain itself is reusable, but a new routing decision
    is made every time route_question() calls ainvoke().
    """
    settings = get_settings()

    model = ChatGoogleGenerativeAI(
        model=settings.gemini_chat_model,
        temperature=0,
        google_api_key=settings.gemini_api_key,
        max_retries=1,
    )

    return ROUTER_PROMPT | model.with_structured_output(RouteDecision)


# Create the router once when the module is loaded.
router_chain = _create_router()


async def route_question(question: str) -> RouteDecision:
    """
    Decide which sources are required for the user's question.

    This function is called for every user question, so every
    question receives a fresh routing decision.
    """
    return await router_chain.ainvoke(
        {"question": question}
    )
