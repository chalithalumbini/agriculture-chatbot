# 🌾 Agriculture Chatbot

A conversational agriculture chatbot built using a static collection of agriculture e-books from Project Gutenberg.

The system uses **Retrieval-Augmented Generation (RAG)** to retrieve relevant information from the books and uses **Llama 3.1 8B** through Ollama to generate answers.

The chatbot can answer questions, handle conversational follow-up questions, and summarize topics across the agriculture books.

---

## 1. Features

The chatbot supports:

- Question answering from the agriculture books
- Conversational follow-up questions
- Semantic search using FAISS
- Topic summarization across multiple books
- Source/book information for generated answers
- Relevance filtering to reduce unsupported answers
- A Streamlit-based chat interface
- A clear conversation option

The chatbot is designed to answer using the provided agriculture books rather than general external knowledge.

---

## 2. Dataset

The assignment provided seven Project Gutenberg links. One book (`40190`) was listed twice, so the knowledge base contains **six unique books**.

### Books used

1. **Pleasant Talk About Fruits, Flowers and Farming**  
   Henry Ward Beecher  
   https://www.gutenberg.org/ebooks/56640

2. **Field, Forest and Farm**  
   Jean-Henri Fabre  
   https://www.gutenberg.org/ebooks/67813

3. **Agriculture for Beginners**  
   Charles William Burkett, Frank Lincoln Stevens, Daniel Harvey Hill  
   https://www.gutenberg.org/ebooks/20772

4. **Science and Practice in Farm Cultivation**  
   James Buckman  
   https://www.gutenberg.org/ebooks/40190

5. **Dry-Farming**  
   John Andreas Widtsoe  
   https://www.gutenberg.org/ebooks/4924

6. **The Farm That Won't Wear Out**  
   Cyril G. Hopkins  
   https://www.gutenberg.org/ebooks/4525

---

## 3. System Architecture

```text
Project Gutenberg Books
          │
          ▼
    Download Books
          │
          ▼
     Preprocessing
          │
          ▼
       Chunking
          │
          ▼
 Sentence Transformer
      Embeddings
          │
          ▼
      FAISS Index
          │
          ▼
     User Question
          │
          ▼
 Conversation / Query
      Rewriting
          │
          ▼
 Semantic Retrieval
          │
          ▼
 Relevance Filtering
          │
          ▼
    Llama 3.1 8B
       + Ollama
          │
          ▼
      Final Answer
          │
          ▼
       Sources