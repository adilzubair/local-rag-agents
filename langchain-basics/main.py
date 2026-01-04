import requests
from dataclasses import dataclass
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool, ToolRuntime
import os 

load_dotenv()

@dataclass
class Context:
    user_id: str

@dataclass
class ResponseFormat:
    summary: str
    temperature_celsius: float
    temperature_fahrenheit: float
    humidity: float

model = init_chat_model('gpt-5-nano', temperature=0.7)

checkpointer = InMemorySaver()


WEATHER_API = os.getenv("WEATHER_API_KEY")

@tool('get_weather', description="Returns weather information of a given city")
def get_weather(city: str):
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={city}"
    )
    
    data = response.json()
    return data

@tool('locate_user', description='Look up a users city based on context')
def locate_user(runtime: ToolRuntime[Context]):
    match runtime.context.user_id:
        case 'ABC123':
            return 'Vienna'
        case 'XYZ456':
            return 'Paris'
        case _:
            return 'Unknown'
    

agent = create_agent(
    model= model,
    tools = [get_weather, locate_user],
    system_prompt='you are a weather assistant who always cracks jokes and is humorous while remaining helpful',
    context_schema=Context,
    response_format=ResponseFormat,
    checkpointer=checkpointer 
)

config = {'configurable': {'thread_id': 1}}

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'what is the weather like?'} 
    ]},
    config = config,                                #type: ignore
    context = Context(user_id='ABC123')
)

print(response['structured_response'])

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'And is this usual?'} 
    ]},
    config = config,                                #type: ignore
    context = Context(user_id='ABC123')
)

print(response['structured_response'].summary)