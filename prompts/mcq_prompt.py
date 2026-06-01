def build_prompt(
    context,
    difficulty,
    weak_topics
):

    return f"""
You are an expert university professor.

SYLLABUS CONTENT:
{context}

STUDENT WEAK TOPICS:
{weak_topics}

DIFFICULTY:
{difficulty}

Generate exactly 10 MCQs.

Requirements:

- Cover the syllabus.
- Prioritize weak topics.
- 4 options each.
- One correct answer.
- Include explanation.
- Avoid duplicates.

Return valid markdown.

Format:

## Question 1

Question

A)
B)
C)
D)

Correct Answer:
Explanation:

Continue until Question 10.
"""