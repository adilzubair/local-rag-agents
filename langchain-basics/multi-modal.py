from dotenv import load_dotenv
from base64 import b64encode
from langchain.chat_models import init_chat_model

load_dotenv()

model = init_chat_model('gpt-5-nano')

message = {
    'role': 'user',
    'content' : [
        {'type': 'text', 'text' : 'Describe the contents of this image'},
        {'type': 'image', 'url': 'https://img.freepik.com/free-photo/closeup-scarlet-macaw-from-side-view-scarlet-macaw-closeup-head_488145-3540.jpg?semt=ais_hybrid&w=740&q=80'}
    ]
}

response = model.invoke([message])

print(response.content)