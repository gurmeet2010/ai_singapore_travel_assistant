import os

from google import genai
from dotenv import load_dotenv

from app.rag.retriever import retrieve_documents

# --------------------------------------------------------------------------- # 
# 1. Load environment variables #
load_dotenv() 
 


# ---------------------------------------------------------------------------
# 1. Gemini Client
# ---------------------------------------------------------------------------

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

if not GEMINI_API_KEY: 
    raise ValueError( "GEMINI_API_KEY is not configured in the .env file" ) 

client = genai.Client( api_key = GEMINI_API_KEY )

MODEL_NAME = "gemini-3.8-flash"


# ---------------------------------------------------------------------------
# 2. Prompt
# ---------------------------------------------------------------------------

PROMPT = """
You are a Singapore Travel Assistant.

Answer the user's question using ONLY the
information provided in the Knowledge Base.

If the Knowledge Base does not contain enough
information to answer the question, say:

"I don't have enough information in my knowledge base
to answer that."

Do not invent facts.

Knowledge Base:
----------------
{context}
----------------

User Question:
{question}

Provide a clear and useful answer.
"""


# ---------------------------------------------------------------------------
# 3. Ask Question
# ---------------------------------------------------------------------------

def ask(question: str):

    # ---------------------------------------------------------
    # Step 1: Retrieve relevant documents from vector database
    # ---------------------------------------------------------

    documents = retrieve_documents(question)

    # ---------------------------------------------------------
    # Step 2: Build Knowledge Base context
    # ---------------------------------------------------------

    context_parts = []

    for document in documents:

        title = document.metadata.get(
            "title",
            "Unknown source"
        )

        url = document.metadata.get(
            "url",
            ""
        )

        context_parts.append(
            f"""
Source: {title}
URL: {url}

Content:
{document.page_content}
"""
        )

    context = "\n\n".join(context_parts)

    # ---------------------------------------------------------
    # Step 3: Create final prompt
    # ---------------------------------------------------------

    final_prompt = PROMPT.format(
        question=question,
        context=context
    )

    # ---------------------------------------------------------
    # Step 4: Send request to Gemini
    # ---------------------------------------------------------

    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=final_prompt
    )

    # ---------------------------------------------------------
    # Step 5: Return answer + sources
    # ---------------------------------------------------------

    return {
        "answer": interaction.output_text,
        "sources": [
            {
                "title": doc.metadata.get("title"),
                "url": doc.metadata.get("url")
            }
            for doc in documents
        ]
    }

