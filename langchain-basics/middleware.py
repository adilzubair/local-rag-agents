from dataclasses import dataclass
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import ModelRequest, ModelResponse, dynamic_prompt

load_dotenv()

@dataclass
class Context:
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    user_role = request.runtime.context.user_role           #type: ignore

    base_prompt = 'You are a helpful and very concise assistant'

    match user_role:
        case 'expert':
            return f'{base_prompt} Provide detailed technical response'
        case 'beginner':
            return f'{base_prompt} Keep you explanation simple and basic'
        case 'child':
            return f'{base_prompt} Explain everything as if you are explaining to a 5 year old'
        case _:
            return base_prompt

agent = create_agent(
    model = 'gpt-5-nano',
    middleware = [user_role_prompt],            #type: ignore
    context_schema = Context
)

response = agent.invoke({
    'messages' : [{'role': 'user', 'content': 'Explain bitcoin'}]
}, context = Context(user_role='expert'))

print(response['messages'][-1].content)




response = agent.invoke({
    'messages' : [{'role': 'user', 'content': 'Explain bitcoin'}]
}, context = Context(user_role='child'))

print(response['messages'][-1].content)

