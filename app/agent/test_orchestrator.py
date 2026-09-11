import asyncio

from app.agent.orchestrator import answer_question


async def main():

    session_id = "test-session"

    questions = [
        "Create a 7-day Singapore itinerary and convert INR 50,000 to SGD."
        #"What are the best attractions in Singapore?",
        #"What is the weather in Singapore?",
        #"Convert 100 USD to SGD.",
        #"Give me a 3-day Singapore itinerary and tell me the weather."
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print(f"QUESTION: {question}")

        result = await answer_question(
            session_id=session_id,
            question=question,
        )

        print("\nANSWER:")
        print(result["answer"])

        print("\nROUTING:")
        print(result["intent"])

        print("\nTOOLS USED:")
        print(result["tools_used"])

        print("\nSOURCES:")
        print(result["sources"])


if __name__ == "__main__":
    asyncio.run(main())