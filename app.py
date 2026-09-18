import os
import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb
from google import genai


# -----------------------------
# PAGE SETTINGS
# -----------------------------

st.set_page_config(
    page_title="Technical Documentation Assistant",
    page_icon="📚"
)

st.title("📚 Technical Documentation Assistant")
st.write("Ask questions about the Python documentation.")


# -----------------------------
# GEMINI CLIENT
# -----------------------------

api_key = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=api_key)


# -----------------------------
# READ PDF
# -----------------------------

@st.cache_resource
def load_document():

    pdf_path = "documents/python_documentation.pdf"

    reader = PdfReader(pdf_path)

    all_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            all_text += text + "\n"

    return all_text


# -----------------------------
# CREATE CHUNKS
# -----------------------------

def create_chunks(text):

    chunk_size = 1000
    overlap = 200

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start = end - overlap

    return chunks


# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

@st.cache_resource
def load_model():

    return SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# LOAD CHROMADB
# -----------------------------

@st.cache_resource
def load_database():

    db_client = chromadb.PersistentClient(
        path="chroma_db"
    )

    collection = db_client.get_or_create_collection(
        name="python_documentation"
    )

    return collection


# -----------------------------
# LOAD COMPONENTS
# -----------------------------

text = load_document()

chunks = create_chunks(text)

model = load_model()

collection = load_database()


# -----------------------------
# CREATE DATABASE IF EMPTY
# -----------------------------

if collection.count() == 0:

    with st.spinner("Preparing documentation..."):

        embeddings = model.encode(chunks)

        collection.add(
            ids=[str(i) for i in range(len(chunks))],
            documents=chunks,
            embeddings=embeddings.tolist()
        )


# -----------------------------
# USER QUESTION
# -----------------------------

question = st.text_input(
    "Enter your question:"
)


# -----------------------------
# RAG PROCESS
# -----------------------------

if question:

    with st.spinner("Searching documentation..."):

        # Convert question into embedding
        question_embedding = model.encode(
            [question]
        )[0]

        # Retrieve relevant chunks
        results = collection.query(
            query_embeddings=[
                question_embedding.tolist()
            ],
            n_results=3
        )

        relevant_documents = results["documents"][0]


    # -----------------------------
    # CREATE CONTEXT
    # -----------------------------

    context = "\n\n".join(
        relevant_documents
    )


    # -----------------------------
    # PROMPT
    # -----------------------------

    prompt = f"""
You are a technical documentation assistant.

Answer the user's question using ONLY the
documentation provided below.

If the answer cannot be found in the
documentation, say:

"I could not find this information in
the provided documentation."

Do not use outside knowledge.

DOCUMENTATION:
{context}

USER QUESTION:
{question}
"""


    # -----------------------------
    # GEMINI GENERATION
    # -----------------------------

    with st.spinner("Generating answer..."):

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


    # -----------------------------
    # DISPLAY ANSWER
    # -----------------------------

    st.subheader("Answer")

    st.write(response.text)


    # -----------------------------
    # DISPLAY SOURCES
    # -----------------------------

    with st.expander("View Retrieved Documentation"):

        for i, document in enumerate(
            relevant_documents
        ):

            st.write(
                f"**Source {i + 1}**"
            )

            st.write(document)