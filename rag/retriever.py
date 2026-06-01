from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings


def get_retriever(persist_dir):

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma(
        persist_directory=persist_dir,
        embedding_function=embeddings
    )

    return db.as_retriever(
        search_kwargs={"k": 5}
    )