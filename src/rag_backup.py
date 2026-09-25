from retriever import Retriever
from llm import generate


retriever = Retriever()


def answer_question(question: str, top_k: int = 5):
    results = retriever.search(
        question,
        top_k=top_k
    )

    context_parts = []

    for i, result in enumerate(results, start=1):

        # Use only the most relevant part of each retrieved chunk.
        text = result["text"][:1800]

        context_parts.append(
            f"""
SOURCE {i}
BOOK: {result['title']}
AUTHOR: {result['author']}

PASSAGE:
{text}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are an agriculture question-answering assistant.

Answer the user's question directly.

The user has asked ONE question:

"{question}"

Use the passages below as your source material.

Rules:
- Answer the question directly.
- Do not create new questions.
- Do not ask the user to clarify this question.
- Combine information from the passages when appropriate.
- Do not invent information that is not supported by the passages.
- If the passages do not contain enough information, say so.
- Keep the answer concise and clear.
- Mention the relevant book title(s) when appropriate.

RETRIEVED PASSAGES:

{context}

Now write the answer to the user's original question.

ANSWER:
"""

    answer = generate(prompt)

    return answer, results