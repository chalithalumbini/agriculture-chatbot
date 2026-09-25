import streamlit as st

from rag import answer_question, summarize_topic


st.set_page_config(
    page_title="Agriculture Chatbot",
    page_icon="🌾",
    layout="centered",
)


# ---------------------------------------------------------
# Page title
# ---------------------------------------------------------

st.title("🌾 Agriculture Chatbot")
st.caption(
    "Ask questions and summarize topics from the agriculture books."
)


# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

with st.sidebar:
    st.header("📚 Knowledge Base")

    st.write("This chatbot uses six agriculture books:")

    books = [
        "Agriculture for Beginners",
        "Dry-Farming",
        "The Farm That Won't Wear Out",
        "Science and Practice in Farm Cultivation",
        "Field, Forest and Farm",
        "Pleasant Talk About Fruits, Flowers and Farming",
    ]

    for book in books:
        st.write(f"• {book}")

    st.divider()

    st.header("💬 Conversation")

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------
# Initialize conversation history
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Display conversation
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if (
            message["role"] == "assistant"
            and "sources" in message
        ):
            with st.expander("📚 Sources"):

                for source in message["sources"]:
                    st.write(
                        f"**{source['title']}** — "
                        f"{source['author']}"
                    )


# ---------------------------------------------------------
# User input
# ---------------------------------------------------------

question = st.chat_input(
    "Ask a question or request a topic summary..."
)


if question:

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": question,
    })

    question_lower = question.lower()

    # Detect summary requests
    summary_words = [
        "summarize",
        "summary",
        "summarise",
        "overview",
    ]

    is_summary = any(
        word in question_lower
        for word in summary_words
    )

    # Generate response
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching the books and generating an answer..."
        ):

            if is_summary:

                answer, sources = summarize_topic(
                    question,
                    top_k=8,
                )

            else:

                answer, sources = answer_question(
                    question,
                    st.session_state.messages[:-1],
                )

        st.markdown(answer)

        # Display sources
        with st.expander("📚 Sources"):

            for source in sources:
                st.write(
                    f"**{source['title']}** — "
                    f"{source['author']}"
                )

    # Save assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })