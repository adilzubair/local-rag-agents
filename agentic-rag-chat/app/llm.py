from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config.settings import settings

class LLMService:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.chat_model
        self.llm = ChatOllama(model=self.model_name)
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Dont use fetch context for greetings and goodbyes, answer normally. Use the provided context to answer the user's question accurately. If the context doesn't contain the answer, say you don't know based on the documents, Only answer questions that are related to the context"),
            MessagesPlaceholder(variable_name="history"),
            ("user", "Context:\n{context}\n\nQuestion: {query}")
        ])

    def generate_response(self, query: str, context_chunks: list, history: list = None) -> str:
        # Combine chunks into a single context string
        context_text = "\n\n".join([c.page_content for c in context_chunks])
        
        # Format history
        formatted_history = []
        if history:
            for msg in history:
                # Handle both Pydantic models (from API) and dicts (if called directly)
                role = msg.role if hasattr(msg, 'role') else msg.get('role')
                content = msg.content if hasattr(msg, 'content') else msg.get('content')
                
                if role == "user":
                    formatted_history.append(HumanMessage(content=content))
                elif role == "assistant":
                    formatted_history.append(AIMessage(content=content))
        
        # Create the chain
        chain = self.prompt_template | self.llm
        
        # Invoke the chain
        response = chain.invoke({
            "context": context_text, 
            "query": query,
            "history": formatted_history
        })
        
        return response.content
