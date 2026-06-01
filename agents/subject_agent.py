import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv("GROQ_API_KEY")
)


class SubjectAgent:

    def detect_subject(self, text):

        prompt = f"""
        Analyze the syllabus below.

        Return ONLY:

        Subject:
        Main Topics:

        Syllabus:
        {text[:4000]}
        """

        response = llm.invoke(prompt)

        return response.content