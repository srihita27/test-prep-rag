import os

import streamlit as st

from rag.pdf_loader import load_pdf

from rag.vector_store import (
    create_vector_store
)

from orchestration.graph import graph

st.title(
    "AI Test Preparation Engine"
)

student_id = st.number_input(
    "Student ID",
    value=1
)

difficulty = st.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

pdf = st.file_uploader(
    "Upload Syllabus PDF",
    type=["pdf"]
)

if st.button("Generate Test"):

    if pdf is None:
        st.error("Upload a PDF first.")
        st.stop()

    os.makedirs("uploads", exist_ok=True)
    os.makedirs("chroma_db", exist_ok=True)

    file_path = os.path.join(
        "uploads",
        pdf.name
    )

    with open(file_path, "wb") as f:
        f.write(pdf.getbuffer())

    docs = load_pdf(file_path)

    pdf_name = pdf.name.replace(
        ".pdf",
        ""
    )

    persist_dir = create_vector_store(
        docs,
        pdf_name
    )

    result = graph.invoke(
        {
            "student_id": student_id,
            "subject": pdf_name,
            "difficulty": difficulty,
            "persist_dir": persist_dir
        }
    )

    st.write(result["mcqs"])