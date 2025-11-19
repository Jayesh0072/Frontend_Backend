from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from vector_store import VectorStore
from file import File

import os

os.environ["OPENAI_API_KEY"] = "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"


class ChatBot:
    def __init__(self, file: File = None, filename: str = None):
        self.vector_store = VectorStore(os.getcwd())

        if file is not None:
            self.vector_store.parse_file(file.content, file.type, file.name)

        if filename is not None:
            with open(filename, "rb") as file:
                self.vector_store.parse_file(file, filename.split(".")[-1], filename)

        template = """Use the following pieces of context to answer the users question.
                      If you don't know the answer, just say that you don't know, don't try to make up an answer.
                      Do not give any information that is not provided in the context.
                      {context}
                      Question: {question}
                      Helpful Answer:"""
        retriever = self.vector_store.get_vector_store().as_retriever(search_type="similarity", search_kwargs={"k": 12})
        self.conv_interface = ConversationalRetrievalChain.from_llm(
            ChatOpenAI(temperature=0.1),
            retriever=retriever,
            combine_docs_chain_kwargs={"prompt": PromptTemplate.from_template(template)},
            return_generated_question=True)
        self.chat_history = []

    def ask(self, question):
        result = self.conv_interface({"question": question, "chat_history": self.chat_history})
        self.chat_history.append((question, result["answer"]))
        return result["answer"]

    def add_history(self, history):
        self.chat_history.extend(history)

    def get_last_question(self):
        return self.chat_history[-1][0]

    def get_last_response(self):
        return self.chat_history[-1][1]

