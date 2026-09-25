from retriever import Retriever
from llm import generate

retriever = Retriever()


def rewrite_query(question: str, conversation_history: list) -> str:
    """
    Convert a follow-up question into a standalone search query.
    """

    if not conversation_history:
        return question

    # Avoid an extra LLM call for clearly standalone questions
    follow_up_phrases = [
        "what about",
        "how about",
        "and what",
        "what does it say about",
        "how does it relate",
        "why is this",
        "what is this",
        "what are these",
        "tell me more",
    ]

    question_lower = question.lower().strip()

    if not any(
        phrase in question_lower
        for phrase in follow_up_phrases
    ):
        return question

    history_text = "\n".join(
        f"{item['role'].upper()}: {item['content']}"
        for item in conversation_history[-6:]
    )

    prompt = f"""
Rewrite the user's latest question into a standalone search query.

Use the conversation history only to understand references such as:
- it
- they
- this
- that
- the previous topic
- the book being discussed

Do not answer the question.
Do not add information.
Return ONLY the rewritten standalone query.

CONVERSATION HISTORY:
{history_text}

LATEST USER QUESTION:
{question}

STANDALONE SEARCH QUERY:
"""

    rewritten = generate(prompt).strip()

    return rewritten


def answer_question(
    question: str,
    conversation_history: list | None = None,
    top_k: int = 5,
):
    """
    Retrieve relevant book passages and generate an answer.
    """

    if conversation_history is None:
        conversation_history = []

    # Convert follow-up questions into standalone queries
    search_query = rewrite_query(
        question,
        conversation_history
    )

    print(f"\nSEARCH QUERY: {search_query}")

    # Retrieve relevant passages
    results = retriever.search(
        search_query,
        top_k=top_k
    )

    # Remove weakly related passages
    results = [
        result
        for result in results
        if result["score"] >= 0.55
    ]

    # Do not let the LLM answer using unrelated passages
    if not results:
        return (
            "I couldn't find relevant information about this "
            "question in the agriculture books.",
            [],
        )

    context_parts = []

    for i, result in enumerate(results, start=1):
        text = result["text"][:1800]

        context_parts.append(
            f"""
SOURCE {i}
BOOK: {result['title']}
AUTHOR: {result['author']}
RELEVANCE SCORE: {result['score']:.4f}

PASSAGE:
{text}
"""
        )

    context = "\n".join(context_parts)

    # Include recent conversation for conversational answers
    history_text = "\n".join(
        f"{item['role'].upper()}: {item['content']}"
        for item in conversation_history[-6:]
    )

    prompt = f"""
You are an agriculture question-answering assistant.

Answer the user's latest question using only the retrieved
passages from the provided agriculture books.

CONVERSATION HISTORY:
{history_text}

LATEST USER QUESTION:
{question}

RETRIEVED PASSAGES:

{context}

RULES:
- Answer the latest user question directly.
- Use the conversation history only to understand context.
- Use only information supported by the retrieved passages.
- Do not use outside knowledge.
- Do not invent information.
- If the passages do not contain enough information to answer
  the question, say that the books do not provide enough
  information.
- Keep the answer clear and reasonably concise.
- Mention relevant book titles when appropriate.
- Do not create additional questions.

ANSWER:
"""

    answer = generate(prompt)

    return answer, results


def summarize_topic(topic: str, top_k: int = 8):
    """
    Retrieve relevant passages about a topic and generate
    a cross-book summary.
    """

    print(f"\nSUMMARY SEARCH: {topic}")

    # Retrieve the most relevant passages
    results = retriever.search(
        topic,
        top_k=top_k
    )

    # Remove weakly related passages
    results = [
        result
        for result in results
        if result["score"] >= 0.55
    ]

    if not results:
        return (
            "I couldn't find sufficiently relevant information "
            "about this topic in the agriculture books.",
            [],
        )

    context_parts = []

    for i, result in enumerate(results, start=1):
        text = result["text"][:1800]

        context_parts.append(
            f"""
SOURCE {i}
BOOK: {result['title']}
AUTHOR: {result['author']}
RELEVANCE SCORE: {result['score']:.4f}

PASSAGE:
{text}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are an agriculture research assistant.

Summarize the following topic using the retrieved passages
from the agriculture books.

TOPIC:
{topic}

RETRIEVED PASSAGES:
{context}

RULES:
- Summarize the topic using only passages that are directly
  relevant to the topic.
- Do not use a passage merely because it comes from one of
  the books.
- Compare ideas from different books when the passages
  support the comparison.
- Do not invent information.
- Do not use outside knowledge.
- Mention only books that contain relevant evidence for
  the topic.
- Keep the summary clear and organized.
- Keep the summary to about 4-6 short paragraphs or
  bullet points.
- Focus on the main ideas rather than repeating details.
- If the retrieved passages are insufficient, say so.

SUMMARY:
"""

    summary = generate(prompt)

    return summary, results