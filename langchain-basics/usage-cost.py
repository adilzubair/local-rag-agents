from langchain_openai import ChatOpenAI, OpenAI
from langchain_community.callbacks import get_openai_callback
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    # api_key="...",
    # base_url="...",
    # organization="...",
    # other params...
)

messages = [
            (
                "system",
                "You are a helpful translator. Translate the user sentence to French.",
            ),
            ("human", "I love programming."),
        ]

with get_openai_callback() as cb:
    result=model.invoke(messages)
    print(result)
    print(f"Total Tokens: {cb.total_tokens}")
    print(f"Prompt Tokens: {cb.prompt_tokens}")
    print(f"Completion Tokens: {cb.completion_tokens}")
    print(f"Total Cost (USD): ${cb.total_cost}")
