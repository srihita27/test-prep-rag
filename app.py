import os
import streamlit as st

from rag.pdf_loader import load_pdf
from rag.vector_store import create_vector_store

from orchestration.graph import graph

from agents.student_agent import StudentAgent


st.set_page_config(
    page_title="AI Test Preparation Engine",
    layout="wide"
)

st.title("AI Test Preparation Engine")

# ==========================
# STUDENT MANAGEMENT
# ==========================

student_agent = StudentAgent()

students = student_agent.get_all_students()

student_options = {
    f"{s['name']} (ID: {s['student_id']})":
    s["student_id"]
    for s in students
}

st.subheader("Select Student")

selected_student = st.selectbox(
    "Available Students",
    list(student_options.keys())
)

student_id = student_options[selected_student]

# ==========================
# ENROLL NEW STUDENT
# ==========================

with st.expander("Enroll New Student"):

    new_name = st.text_input(
        "Student Name"
    )

    if st.button("Enroll Student"):

        if new_name.strip():

            new_id = (
                student_agent
                .enroll_student(new_name)
            )

            st.success(
                f"Student enrolled successfully! New ID: {new_id}"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter a valid name."
            )

# ==========================
# TEST SETTINGS
# ==========================

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

# ==========================
# GENERATE TEST
# ==========================

if st.button("Generate Test"):

    if pdf is None:

        st.error(
            "Please upload a syllabus PDF."
        )

        st.stop()

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    os.makedirs(
        "chroma_db",
        exist_ok=True
    )

    file_path = os.path.join(
        "uploads",
        pdf.name
    )

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            pdf.getbuffer()
        )

    with st.spinner(
        "Processing syllabus..."
    ):

        docs = load_pdf(
            file_path
        )

        pdf_name = (
            pdf.name
            .replace(".pdf", "")
        )

        persist_dir = (
            create_vector_store(
                docs,
                pdf_name
            )
        )

        result = graph.invoke(
            {
                "student_id": student_id,
                "subject": pdf_name,
                "difficulty": difficulty,
                "persist_dir": persist_dir
            }
        )

    st.session_state["questions"] = (
        result["mcqs"]
    )

# ==========================
# DISPLAY TEST
# ==========================

if "questions" in st.session_state:

    questions = (
        st.session_state["questions"]
    )

    st.divider()

    st.header("Generated Test")

    for i, q in enumerate(questions):

        st.subheader(
            f"Question {i+1}"
        )

        answer = st.radio(
            f"{q['question']}",
            list(
                q["options"].keys()
            ),
            format_func=lambda x:
            f"{x}. {q['options'][x]}",
            key=f"q{i}",
            index=None
        )

        if st.button(
            f"Check Answer {i+1}",
            key=f"check{i}"
        ):

            # No option selected
            if answer is None:

                st.warning(
                    "⚠️ Please select an option first."
                )

            # Correct answer
            elif answer == q["correct"]:

                st.success(
                    "✅ Correct Answer"
                )

                st.info(
                    f"Explanation: {q['explanation']}"
                )

            # Wrong answer
            else:

                st.error(
                    "❌ Wrong Answer"
                )

                st.write(
                    f"**Correct Answer:** "
                    f"{q['correct']}. "
                    f"{q['options'][q['correct']]}"
                )

                st.info(
                    f"Explanation: {q['explanation']}"
                )