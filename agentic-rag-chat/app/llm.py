from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from config.settings import settings

class LLMService:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or settings.chat_model
        self.llm = ChatOllama(model=self.model_name)
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI assistant. Dont use fetch context for greetings and goodbyes, answer normally. Use the provided context to answer the user's question accurately. If the context doesn't contain the answer, say you don't know based on the documents, Only answer questions that are related to the context"),
            ("user", "Context:\n{context}\n\nQuestion: {query}")
        ])

    def generate_response(self, query: str, context_chunks: list) -> str:
        # Combine chunks into a single context string
        context_text = "\n\n".join([c.page_content for c in context_chunks])
        
        # Create the chain
        chain = self.prompt_template | self.llm
        
        # Invoke the chain
        response = chain.invoke({"context": context_text, "query": query})
        
        return response.content
