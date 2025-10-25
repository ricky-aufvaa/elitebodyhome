
from langchain_core.prompts import ChatPromptTemplate
from langchain.messages import HumanMessage
from llm import get_chat_model

def rag_chain():
    llm = get_chat_model()

    template = """Answer the question based on the following context and the Chathistory. Especially take the latest question into consideration:

    Chathistory: {history}

    Context: {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    rag_chain = prompt | llm
    return rag_chain

# if __name__ =="__main__":
#     rag_chain().invoke(HumanMessage(cont)"How to make my skin better")