from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from backend.app.core.settings import Settings
from backend.app.db.vector_store import VectorStoreFactory


class RetrievalService:
    def __init__(self, settings: Settings, vector_factory: VectorStoreFactory) -> None:
        self.settings = settings
        self.vector_factory = vector_factory
        self.llm = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            temperature=settings.openai_temperature,
        )

    def ask(self, question: str) -> tuple[str, list]:
        store = self.vector_factory.load()
        retriever = store.as_retriever(search_kwargs={"k": self.settings.top_k})

        prompt = ChatPromptTemplate.from_template(
            """
            You are a precise enterprise assistant. Use only the supplied context.
            If the answer is not in the context, say that clearly.

            Context:
            {context}

            Question:
            {input}
            """
        )

        combine_docs_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, combine_docs_chain)

        result = retrieval_chain.invoke({"input": question})
        answer = result.get("answer", "No answer returned.")
        sources = result.get("context", [])
        return answer, sources
