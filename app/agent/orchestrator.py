import json
from typing import Any
from langchain_google_genai import ChatGoogleGenerativeAI
from app.agent.prompts import ANSWER_PROMPT
from app.agent.router import route_question
from app.config import get_settings
from app.memory.conversation import memory
from app.mcp.tools import convert_currency, extract_currency_request, get_weather
from app.rag.retriever import retrieve_documents


def _format_rag_context(documents) -> tuple[str, list[dict[str, str]]]:
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

        source_item = {"source": source, "title": title, "url": url}
        if source_item not in sources:
            sources.append(source_item)

    return "\n\n".join(chunks), sources


def _weather_days_from_question(question: str) -> int:
    q = question.lower()
    if "seven" in q or "7-day" in q or "7 day" in q:
        return 7
    if "five" in q or "5-day" in q or "5 day" in q:
        return 5
    return 3


async def _build_mcp_results(
    sources: list[str],
    question: str,
) -> tuple[str, list[dict[str, Any]]]:
    results = []
    tool_metadata = []

    if "WEATHER_MCP" in sources:
        try:
            weather = await get_weather(_weather_days_from_question(question))
            results.append(
                "WEATHER_MCP RESULT:\n" + json.dumps(weather, indent=2)
            )
            tool_metadata.append(
                {
                    "tool": "get_singapore_weather",
                    "server": "Singapore Weather MCP",
                    "status": "success",
                }
            )
        except Exception as exc:
            results.append(
                "WEATHER_MCP ERROR: Current weather could not be retrieved."
            )
            tool_metadata.append(
                {
                    "tool": "get_singapore_weather",
                    "server": "Singapore Weather MCP",
                    "status": "failed",
                    "error": str(exc),
                }
            )

    if "CURRENCY_MCP" in sources:
        request = extract_currency_request(question)
        if request is None:
            results.append(
                "CURRENCY_MCP ERROR: Could not determine amount and currencies."
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
            amount, from_currency, to_currency = request
            try:
                currency = await convert_currency(
                    amount, from_currency, to_currency
                )
                results.append(
                    "CURRENCY_MCP RESULT:\n" + json.dumps(currency, indent=2)
                )
                tool_metadata.append(
                    {
                        "tool": "convert_currency",
                        "server": "Currency Conversion MCP",
                        "status": "success",
                    }
                )
            except Exception as exc:
                print("cyrrency error",exc)
                results.append(
                    "CURRENCY_MCP ERROR: Current currency conversion "
                    "could not be retrieved."
                )
                tool_metadata.append(
                    {
                        "tool": "convert_currency",
                        "server": "Currency Conversion MCP",
                        "status": "failed",
                        "error": str(exc),
                    }
                )

    return "\n\n".join(results) or "No MCP tools were required.", tool_metadata


async def answer_question(
    session_id: str,
    question: str,
) -> dict[str, Any]:
    decision = await route_question(question)

    rag_context = "RAG was not selected."
    sources = []

    if "RAG" in decision.sources:
        documents = retrieve_documents(question)
        rag_context, sources = _format_rag_context(documents)

    mcp_context, tool_metadata = await _build_mcp_results(
        decision.sources,
        question,
    )

    conversation_context = memory.as_text(session_id)

    settings = get_settings()
    model = ChatGoogleGenerativeAI(
            model=settings.gemini_chat_model,
            temperature=0,
            google_api_key=settings.gemini_api_key,
        )

    chain = ANSWER_PROMPT | model

    response = await chain.ainvoke(
        {
            "question": question,
            "rag_context": rag_context,
            "mcp_context": mcp_context,
            "conversation_context": conversation_context,
        }
    )

    answer = response.content

    memory.add(session_id, "user", question)
    memory.add(session_id, "assistant", answer)

    return {
        "answer": answer,
        "intent": decision.sources,
        "routing_reason": decision.reason,
        "sources": sources,
        "tools_used": tool_metadata,
    }
