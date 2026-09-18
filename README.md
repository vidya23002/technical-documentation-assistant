# Technical Documentation Assistant Using RAG

## Project Overview

The Technical Documentation Assistant is a Retrieval-Augmented Generation (RAG) based chatbot that answers questions from technical documentation.

In this project, Python documentation is used as the knowledge base. The system retrieves relevant sections from the documentation based on the user's question and provides the retrieved information to Google Gemini to generate a grounded answer.

The application is developed using Python and Streamlit.

---

## Problem Statement

Technical documentation contains a large amount of information, making it difficult to quickly find answers to specific questions.

This project provides a chatbot that can:

- Understand questions related to technical documentation.
- Search the documentation based on semantic meaning.
- Retrieve relevant information.
- Generate answers using the retrieved documentation.
- Display the retrieved documentation to the user.
- Avoid using information outside the provided knowledge base.

---

## Objectives

- Build a documentation-based question-answering system.
- Extract text from technical documentation.
- Divide the documentation into smaller chunks.
- Generate embeddings for the documentation.
- Store embeddings in a vector database.
- Perform semantic search.
- Retrieve relevant documentation sections.
- Generate grounded answers using Google Gemini.
- Provide a simple web interface using Streamlit.

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| PyPDF | Extract text from PDF documentation |
| Sentence Transformers | Generate text embeddings |
| ChromaDB | Store and retrieve document embeddings |
| Google Gemini | Generate answers from retrieved context |

---

## System Architecture

```text
Python Documentation PDF
          |
          v
    Text Extraction
          |
          v
     Text Chunking
          |
          v
 Sentence Transformer
          |
          v
      Embeddings
          |
          v
       ChromaDB
          |
          |
    User Question
          |
          v
 Question Embedding
          |
          v
    Semantic Search
          |
          v
 Top 3 Relevant Chunks
          |
          v
    Google Gemini
          |
          v
    Generated Answer


## Complete Workflow
Step 1: Load Python Documentation PDF
                |
                v
Step 2: Extract Text
                |
                v
Step 3: Split Text into Chunks
                |
                v
Step 4: Generate Embeddings
                |
                v
Step 5: Store Embeddings in ChromaDB
                |
                v
Step 6: Accept User Question
                |
                v
Step 7: Generate Question Embedding
                |
                v
Step 8: Perform Semantic Search
                |
                v
Step 9: Retrieve Top 3 Relevant Chunks
                |
                v
Step 10: Provide Context to Gemini
                |
                v
Step 11: Generate Grounded Answer
                |
                v
Step 12: Display Answer and Retrieved Documentation
