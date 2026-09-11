import json
from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI

from app.agent.prompts import ANSWER_PROMPT
from app.agent.router import route_question
from app.config import get_settings
from app.memory.conversation import memory
from app.mcp.tools import (
    convert_currency,
    extract_currency_request,
    get_weather,
)
from app.rag.retriever import retrieve_documents


def _create_answer_chain():
    """
    Create the answer-generation chain once and reuse it.
    """
    settings = get_settings()

    model = ChatGoogleGenerativeAI(
        model=settings.gemini_chat_model,
        temperature=0,
        google_api_key=settings.gemini_api_key,
        max_retries=1,
    )

    return ANSWER_PROMPT | model


# Create the answer chain once when the module is loaded.
answer_chain = _create_answer_chain()


def _format_rag_context(
    documents,
) -> tuple[str, list[dict[str, str]]]:
    """
    Format retrieved RAG documents into LLM context
    and collect their source metadata.
    """
    sources = []
    chunks = []

    for index, doc in enumerate(documents, start=1):
        title = doc.metadata.get("title", "Unknown source")
        url = doc.metadata.get("url", "")
        source = doc.metadata.get("source", "Unknown source")

        chunks.append(
            f"[Chunk {index}]\n"
            f"Source: {source}\n"
            f"Title: {title}\n"
            f"URL: {url}\n"
            f"Content:\n{doc.page_content}"
        )

        source_item = {
            "source": source,
            "title": title,
            "url": url,
        }

        if source_item not in sources:
            sources.append(source_item)

    if not chunks:
        return (
            "No relevant information was found in the knowledge base.",
            [],
        )

    return "\n\n".join(chunks), sources


def _weather_days_from_question(question: str) -> int:
    """
    Determine the requested weather forecast period.
    """
    question_lower = question.lower()

    if (
        "seven" in question_lower
        or "7-day" in question_lower
        or "7 day" in question_lower
    ):
        return 7

    if (
        "five" in question_lower
        or "5-day" in question_lower
        or "5 day" in question_lower
    ):
        return 5

    return 3


async def _build_mcp_results(
    sources: list[str],
    question: str,
) -> tuple[str, list[dict[str, Any]]]:
    """
    Execute the MCP tools selected by the router.
    """
    results = []
    tool_metadata = []

    # ---------------------------------------------------------
    # Weather MCP
    # ---------------------------------------------------------
    if "WEATHER_MCP" in sources:
        try:
            weather = await get_weather(
                _weather_days_from_question(question)
            )

            results.append(
                "WEATHER_MCP RESULT:\n"
                + json.dumps(weather, indent=2)
            )

            tool_metadata.append(
                {
                    "tool": "get_singapore_weather",
                    "server": "Singapore Weather MCP",
                    "status": "success",
                }
            )

        except Exception:
            results.append(
                "WEATHER_MCP ERROR: "
                "Current weather could not be retrieved."
            )

            tool_metadata.append(
                {
                    "tool": "get_singapore_weather",
                    "server": "Singapore Weather MCP",
                    "status": "failed",
                    "error": "Weather service unavailable.",
                }
            )

    # ---------------------------------------------------------
    # Currency MCP
    # ---------------------------------------------------------
    if "CURRENCY_MCP" in sources:
        currency_request = extract_currency_request(question)

        if currency_request is None:
            results.append(
                "CURRENCY_MCP ERROR: "
                "Could not determine amount and currencies."
            )

            tool_metadata.append(
                {
                    "tool": "convert_currency",
                    "server": "Currency Conversion MCP",
                    "status": "failed",
                    "error": "Could not parse currency request.",
                }
            )

        else:
            amount, from_currency, to_currency = currency_request

            try:
                currency = await convert_currency(
                    amount,
                    from_currency,
                    to_currency,
                )

                results.append(
                    "CURRENCY_MCP RESULT:\n"
                    + json.dumps(currency, indent=2)
                )

                tool_metadata.append(
                    {
                        "tool": "convert_currency",
                        "server": "Currency Conversion MCP",
                        "status": "success",
                    }
                )

            except Exception:
                results.append(
                    "CURRENCY_MCP ERROR: "
                    "Current currency conversion could not be retrieved."
                )

                tool_metadata.append(
                    {
                        "tool": "convert_currency",
                        "server": "Currency Conversion MCP",
                        "status": "failed",
                        "error": "Currency service unavailable.",
                    }
                )

    if not results:
        return (
            "No MCP tools were required.",
            tool_metadata,
        )

    return "\n\n".join(results), tool_metadata


async def answer_question(
    session_id: str,
    question: str,
) -> dict[str, Any]:
    """
    Main orchestration workflow.

    1. Route the question.
    2. Retrieve RAG documents if required.
    3. Execute MCP tools if required.
    4. Add conversation history.
    5. Generate the final answer.
    6. Store the conversation.
    """

    # ---------------------------------------------------------
    # 1. Route the question
    # ---------------------------------------------------------
    decision = await route_question(question)

    # ---------------------------------------------------------
    # 2. RAG
    # ---------------------------------------------------------
    rag_context = "RAG was not selected."
    sources = []

    if "RAG" in decision.sources:
        documents = retrieve_documents(question)

        rag_context, sources = _format_rag_context(
            documents
        )

    # ---------------------------------------------------------
    # 3. MCP tools
    # ---------------------------------------------------------
    mcp_context, tool_metadata = await _build_mcp_results(
        decision.sources,
        question,
    )

    # ---------------------------------------------------------
    # 4. Conversation memory
    # ---------------------------------------------------------
    conversation_context = memory.as_text(
        session_id
    )

    # ---------------------------------------------------------
    # 5. Generate final answer
    # ---------------------------------------------------------
    response = await answer_chain.ainvoke(
        {
            "question": question,
            "rag_context": rag_context,
            "mcp_context": mcp_context,
            "conversation_context": conversation_context,
        }
    )

    answer = response.content

    # ---------------------------------------------------------
    # 6. Save conversation
    # ---------------------------------------------------------
    memory.add(
        session_id,
        "user",
        question,
    )

    memory.add(
        session_id,
        "assistant",
        answer,
    )

    # ---------------------------------------------------------
    # 7. Return API response
    # ---------------------------------------------------------
    return {
        "answer": answer,
        "intent": decision.sources,
        "routing_reason": decision.reason,
        "sources": sources,
        "tools_used": tool_metadata,
    }
