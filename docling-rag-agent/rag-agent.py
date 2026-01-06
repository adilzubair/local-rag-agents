# import basics
import os
from dotenv import load_dotenv

# import langchain
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()  


embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),         # type: ignore
)

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),           # type: ignore
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"), 
)

llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0
)

@tool
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)

    serialized = ""
    for doc in retrieved_docs:
        serialized += f"Source: {doc.metadata['source']}\nContent: {doc.page_content}\n\n"

    return serialized

tools = [retrieve]

agent = create_agent(
    model = 'ministral-3:3b',
    tools=tools,
    system_prompt=SystemMessage(
        content=[
            {
                "type": "text",
                "text": "You are an AI assistant tasked with analyzing literary works.",
            },
        ]
    )
    
)