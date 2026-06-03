import os
import json

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from prompts.mcq_prompt import (
    build_prompt
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=os.getenv(
        "GROQ_API_KEY"
    ),
    temperature=0.7
)


class MCQAgent:

    def generate(
        self,
        context,
        difficulty,
        weak_topics
    ):

        prompt = build_prompt(
            context,
            difficulty,
            weak_topics
        )

        response = llm.invoke(
            prompt
        )

        content = (
            response.content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        return json.loads(content)