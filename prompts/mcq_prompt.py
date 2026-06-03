def build_prompt(
    context,
    difficulty,
    weak_topics
):

    return f"""
You are an expert exam setter.

Context:
{context}

Weak Topics:
{weak_topics}

Generate EXACTLY 10 MCQs.

Return ONLY valid JSON.

Example:

[
 {{
   "question":"What is a compiler?",
   "options": {{
      "A":"Option A",
      "B":"Option B",
      "C":"Option C",
      "D":"Option D"
   }},
   "correct":"B",
   "explanation":"Explanation here"
 }}
]

Difficulty:
{difficulty}
"""