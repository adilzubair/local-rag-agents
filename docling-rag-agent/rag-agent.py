# import basics
import os
from dotenv import load_dotenv
from dataclasses import dataclass

# import langchain
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

load_dotenv()

@dataclass
class Context:
    pass  # No chat_history anymore

# Initialize embeddings and vector store
embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL", ""),  # type: ignore
)

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),  # type: ignore
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"),
)

# Initialize model
model = ChatOllama(
    model="ministral-3:3b",
    temperature=0,
)

# Initialize memory (will store context independently)
memory = InMemorySaver()

# Tool for retrieving docs
@tool("retrieve", description="Retrieve relevant documents from the vector store")
def retrieve(query: str):
    print(f"[DEBUG] retrieve() called with: {query}")

    docs = vector_store.similarity_search(query, k=5)

    if not docs:
        return "NO_RELEVANT_CONTEXT"

    serialized = ""
    for doc in docs:
        serialized += (
            f"Source: {doc.metadata.get('source', 'unknown')}\n"
            f"Content: {doc.page_content}\n\n"
        )

    return serialized

# Create agent
agent = create_agent(
    model=model,
    tools=[retrieve],
    system_prompt="""
You are a strict RAG-only assistant.

You MUST follow this procedure for EVERY user query:

1. ALWAYS call the `retrieve` tool with the user query.
2. Read the retrieved content.
3. Answer using ONLY the retrieved content.

Hard rules:
- You are NOT allowed to answer without calling `retrieve`.
- You are NOT allowed to use prior knowledge.
- If the retrieved content does not contain the answer, reply exactly:
  "I don't know."
- Do NOT ask follow-up questions.
- Do NOT explain your reasoning.

Every factual statement MUST be supported by retrieved content.

Required response format (exact):

Answer: ...
Source: ...
""",
    # context_schema=Context,
    checkpointer=memory,
)

# Terminal chat loop (without chat_history)
def run_terminal_chat():
    print("RAG Agent started. Type 'exit' or 'quit' to stop.\n")
    # context = Context()  # Empty context; memory will manage persistence

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in {"exit", "quit"}:
            print("Exiting...")
            break

        # Invoke agent directly without building chat_history
        response = agent.invoke(
            {"messages": [HumanMessage(content=user_input)]},
            # context=context,
            config={"configurable": {"thread_id": 1}},
        )

        # Extract AI message
        ai_message = response["messages"][-1]
        print(f"\nAI: {ai_message.content}\n")


if __name__ == "__main__":
    print("Vector DB document count:", vector_store._collection.count())

    docs = vector_store.similarity_search("bitcoin", k=3)
    print("Retrieved docs:", len(docs))
    for d in docs:
        print(d.metadata, d.page_content[:200])

    run_terminal_chat()
