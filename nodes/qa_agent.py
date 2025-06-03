from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.schema import Document
import os

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=os.environ.get("OPENAI_API_KEY"))

def answer_question(x):
    question = input("💬 Enter your question: ")
    docs = [Document(page_content=chunk) for chunk in x["chunks"]]
    chain = load_qa_chain(llm, chain_type="stuff")
    answer = chain.run(input_documents=docs, question=question)
    return {"qa_answer": answer}