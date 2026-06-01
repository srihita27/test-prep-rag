from typing import TypedDict

from agents.student_agent import StudentAgent

from agents.mcq_agent import MCQAgent

from rag.retriever import get_retriever

from langgraph.graph import (
    StateGraph,
    END
)

class State(TypedDict):

    student_id: int

    subject: str

    difficulty: str

    persist_dir: str

    weak_topics: list

    context: str

    mcqs: str


def student_node(state):

    agent = StudentAgent()

    state["weak_topics"] = (
        agent.get_weak_topics(
            state["student_id"],
            state["subject"]
        )
    )

    return state


def retrieve_node(state):

    retriever = get_retriever(
        state["persist_dir"]
    )

    query = f"""
    Generate {state['difficulty']}
    level MCQs covering the syllabus.
    """

    docs = retriever.invoke(query)

    state["context"] = "\n".join(
        [doc.page_content for doc in docs]
    )

    print("\n========== RETRIEVED ==========")
    print(state["context"][:1000])

    return state


def generate_node(state):

    agent = MCQAgent()

    state["mcqs"] = (
        agent.generate(
            state["context"],
            state["difficulty"],
            state["weak_topics"]
        )
    )

    return state


builder = StateGraph(State)

builder.add_node(
    "student",
    student_node
)

builder.add_node(
    "retrieve",
    retrieve_node
)

builder.add_node(
    "generate",
    generate_node
)

builder.set_entry_point(
    "student"
)

builder.add_edge(
    "student",
    "retrieve"
)

builder.add_edge(
    "retrieve",
    "generate"
)

builder.add_edge(
    "generate",
    END
)

graph = builder.compile()