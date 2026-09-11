from app.rag.qa import ask


def main():

    questions = [
        "What are the must-visit attractions in Singapore?",
        "How can tourists travel around Singapore?",
        "What are some cultural neighbourhoods in Singapore?",
        "What indoor activities are available in Singapore?"
    ]

    for question in questions:

        print("\n")
        print("=" * 80)
        print("QUESTION:")
        print(question)
        print("=" * 80)

        result = ask(question)

        print("\nANSWER:")
        print(result["answer"])

        print("\nSOURCES:")

        for source in result["sources"]:
            print(
                f"- {source['title']}"
            )
            print(
                f"  {source['url']}"
            )


if __name__ == "__main__":
    main()