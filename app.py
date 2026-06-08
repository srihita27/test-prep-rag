import os
import streamlit as st

from rag.pdf_loader import load_pdf
from rag.vector_store import create_vector_store

from orchestration.graph import graph
from agents.student_agent import StudentAgent


# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="PrepPilot AI",
    page_icon="🎓",
    layout="wide"
)

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.title("🎓 PrepPilot AI")

    st.write(
        "Your Intelligent Test Preparation Assistant"
    )

    st.divider()

    st.write(
        """
        **Powered By**
        - Groq
        - LangGraph
        - ChromaDB
        - RAG
        """
    )

# ======================================
# HEADER
# ======================================

st.title("🎓 PrepPilot AI")

st.caption(
    "Generate personalized MCQ tests from any syllabus PDF using AI."
)

st.divider()

# ======================================
# STUDENT MANAGEMENT
# ======================================

student_agent = StudentAgent()

students = student_agent.get_all_students()

student_options = {
    f"{s['name']} (ID: {s['student_id']})":
    s["student_id"]
    for s in students
}

st.subheader("👨‍🎓 Select Student")

selected_student = st.selectbox(
    "Available Students",
    list(student_options.keys())
)

student_id = student_options[selected_student]

# ======================================
# ENROLL STUDENT
# ======================================

with st.expander("➕ Enroll New Student"):

    new_name = st.text_input(
        "Student Name"
    )

    if st.button(
        "Enroll Student"
    ):

        if new_name.strip():

            new_id = (
                student_agent
                .enroll_student(new_name)
            )

            st.success(
                f"Student enrolled successfully! "
                f"New ID: {new_id}"
            )

            st.rerun()

        else:

            st.warning(
                "Please enter a valid name."
            )

# ======================================
# TEST SETTINGS
# ======================================

st.subheader("⚙️ Test Settings")

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

if pdf:

    st.success(
        f"Uploaded: {pdf.name}"
    )

# ======================================
# GENERATE TEST
# ======================================

if st.button("🚀 Generate Test"):

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
        "Analyzing syllabus and generating test..."
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

    st.session_state["results"] = {}

# ======================================
# DISPLAY TEST
# ======================================

if "questions" in st.session_state:

    questions = (
        st.session_state["questions"]
    )

    if "results" not in st.session_state:

        st.session_state["results"] = {}

    st.divider()

    st.header("📝 Generated Test")

    score = sum(
        1
        for result in
        st.session_state["results"].values()
        if result["status"] == "correct"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Current Score",
            f"{score}/{len(questions)}"
        )

    with col2:

        percentage = round(
            (
                score /
                len(questions)
            ) * 100,
            2
        )

        st.metric(
            "Percentage",
            f"{percentage}%"
        )

    st.divider()

    for i, q in enumerate(questions):

        st.subheader(
            f"Question {i+1}"
        )

        answer = st.radio(
            q["question"],
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

            if answer is None:

                st.session_state["results"][i] = {
                    "status": "unanswered"
                }

            elif answer == q["correct"]:

                st.session_state["results"][i] = {
                    "status": "correct",
                    "selected": answer
                }

            else:

                st.session_state["results"][i] = {
                    "status": "wrong",
                    "selected": answer
                }

        # ======================
        # DISPLAY RESULT
        # ======================

        if i in st.session_state["results"]:

            result = (
                st.session_state["results"][i]
            )

            if result["status"] == "unanswered":

                st.warning(
                    "⚠️ Please select an option first."
                )

            elif result["status"] == "correct":

                st.success(
                    "✅ Correct Answer"
                )

                st.write(
                    f"**Your Answer:** "
                    f"{result['selected']}. "
                    f"{q['options'][result['selected']]}"
                )

                st.info(
                    f"Explanation: "
                    f"{q['explanation']}"
                )

            elif result["status"] == "wrong":

                st.error(
                    "❌ Wrong Answer"
                )

                st.write(
                    f"**Your Answer:** "
                    f"{result['selected']}. "
                    f"{q['options'][result['selected']]}"
                )

                st.write(
                    f"**Correct Answer:** "
                    f"{q['correct']}. "
                    f"{q['options'][q['correct']]}"
                )

                st.info(
                    f"Explanation: "
                    f"{q['explanation']}"
                )

        st.divider()

# ======================================
# FOOTER
# ======================================

st.divider()

st.caption(
    "PrepPilot AI © 2026 | Powered by RAG, LangGraph, ChromaDB and Groq"
)