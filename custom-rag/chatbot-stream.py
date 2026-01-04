# import basics
import os
from dotenv import load_dotenv

# import langchain
from langchain.agents import AgentExecutor
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool

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

prompt = PromptTemplate.from_template("""                                
You are a helpful assistant. You will be provided with a query and a chat history.
Your task is to retrieve relevant information from the vector store and provide a response.
For this you use the tool 'retrieve' to get the relevant information.
                                      
The query is as follows:                    
{input}

The chat history is as follows:
{chat_history}

Please provide a concise and informative response based on the retrieved information.
If you don't know the answer, say "I don't know" (and don't provide a source).
                                      
You can use the scratchpad to store any intermediate results or notes.
The scratchpad is as follows:
{agent_scratchpad}

For every piece of information you provide, also provide the source.

Return text as follows:

Answer: Answer of the question
Source: source_url
""")

@tool
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)

    serialized = ""
    for doc in retrieved_docs:
        serialized += f"Source: {doc.metadata['source']}\nContent: {doc.page_content}\n\n"

    return serialized

tools = [retrieve]

agent = create_tool_calling_agent(llm, tools, prompt)  # type: ignore
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# -----------------------------
# Terminal chat loop
# -----------------------------

chat_history = []

print("Agentic RAG Chatbot")
print("Type 'exit' or 'quit' to stop.\n")

while True:
    user_question = input("You: ").strip()

    if user_question.lower() in {"exit", "quit"}:
        print("Goodbye 👋")
        break

    chat_history.append(HumanMessage(user_question))

    result = agent_executor.invoke({
        "input": user_question,
        "chat_history": chat_history
    })

    ai_message = result["output"]
    print(f"\nAssistant:\n{ai_message}\n")

    chat_history.append(AIMessage(ai_message))
