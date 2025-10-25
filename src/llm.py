#Define the llm
from langchain_aws import ChatBedrock
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
load_dotenv()

def get_chat_model():
    """
    Initialize the Bedrock client with Claude sonnet 4
    """
    return ChatBedrock(
        model_id=os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-sonnet-4-20250514-v1:0"),
        region_name=os.getenv("AWS_REGION"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        model_kwargs={
            "max_tokens": 4096,
            "temperature": 0.3,
            "top_p": 0.9
        }
    )

def get_retriever():
    embedding_function = BedrockEmbeddings()
    db = FAISS.load_local("faiss_embeddings",embeddings=embedding_function,allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="mmr",search_kwargs = {"k":4})
    return retriever

