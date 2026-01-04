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






WEATHER_API = os.getenv("WEATHER_API_KEY")

@tool('get_weather', description="Returns weather information of a given city")
def get_weather(city: str):
    response = requests.get(
        f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API}&q={city}"
    )
    
    data = response.json()
    return data
    

agent = create_agent(
    model='gpt-5-nano',
    tools = [get_weather],
    system_prompt='you are a weather assistant who always cracks jokes and is humorous while remaining helpful'
)

response = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'what is the weather like in dubai?'} 
    ]
})

print(response)
print(response['messages'][-1].content)