from app.rag.retriever import retrieve_documents


def main():

    questions = [
        "What are the must-visit attractions in Singapore?",
        "How can tourists travel around Singapore?",
        "What neighbourhoods are good for cultural experiences?",
        "What indoor activities are available?",
        "Suggest a three-day Singapore itinerary."
    ]

    for question in questions:

        print("\n" + "=" * 80)

        print("QUESTION:")
        print(question)

        print("=" * 80)

        documents = retrieve_documents(question)

        print(
            f"\nRetrieved {len(documents)} chunks\n"
        )

        for index, document in enumerate(
            documents,
            start=1
        ):

            print("-" * 80)

            print(
                f"CHUNK {index}"
            )

            print(
                "Title:",
                document.metadata.get(
                    "title"
                )
            )

            print(
                "URL:",
                document.metadata.get(
                    "url"
                )
            )

            print("\nContent:")

            print(
                document.page_content[:800]
            )


if __name__ == "__main__":
    main()