import asyncio

from app.agent.router import route_question


async def main():

    questions = [
        #"What are the best attractions in Singapore?",
        #"What is the weather in Singapore?",
        #"Convert 100 USD to SGD.",
        "Give me a 3-day Singapore itinerary and tell me the weather."
    ]

    for question in questions:

        print("\n" + "=" * 70)
        print(f"Question: {question}")

        decision = await route_question(question)

        print(f"Sources: {decision.sources}")
        print(f"Reason: {decision.reason}")


if __name__ == "__main__":
    asyncio.run(main())