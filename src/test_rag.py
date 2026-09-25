from rag import answer_question


def main():
    conversation_history = []

    # First question
    question1 = "How can soil fertility be maintained?"

    answer1, sources1 = answer_question(
        question1,
        conversation_history
    )

    print("\nUSER:")
    print(question1)

    print("\nASSISTANT:")
    print(answer1)

    # Save first exchange
    conversation_history.append({
        "role": "user",
        "content": question1
    })

    conversation_history.append({
        "role": "assistant",
        "content": answer1
    })

    # Follow-up question
    question2 = "What about dry-farming?"

    answer2, sources2 = answer_question(
        question2,
        conversation_history
    )

    print("\nUSER:")
    print(question2)

    print("\nASSISTANT:")
    print(answer2)

    print("\nSOURCES FOR FOLLOW-UP:")
    for source in sources2:
        print(
            f"- {source['title']} "
            f"({source['author']}) "
            f"[{source['chunk_id']}] "
            f"score={source['score']:.4f}"
        )


if __name__ == "__main__":
    main()