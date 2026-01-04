from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_community. vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain.agents import create_agent

load_dotenv()

embeddings = OpenAIEmbeddings(model='text-embedding-3-large')

texts = [
'I love apples.',
'I enjoy oranges.'
'I think pears taste very good.',
'I hate bananas.',
'I dislike raspberries.',
'I despise mangos.',
'I love Linux.'
'I hate Windows.'
]

vector_store = FAISS.from_texts(texts, embedding=embeddings)
print(vector_store.similarity_search('What fruits does the person like?', k=3))
print(vector_store.similarity_search('What fruits does the person hate?', k=3))


retriever = vector_store.as_retriever(search_kwargs = {'k': 3})

retriever_tool = create_retriever_tool(retriever=retriever, name='kb_search', description='search the small product / fruit database for information')


agent = create_agent(
    model = 'gpt-5-mini',
    tools = [retriever_tool],
    system_prompt=(
        "you are a helpful assistant, for questions about fruits or devices first call the kb_search tool to retrieve the context, then answer based on that. maybe you have to use the tool multiple times before answering."
    )
)

result = agent.invoke({
    'messages': [
        {'role': 'user', 'content': 'what fruits do i like and what fruits do i dislike'} 
    ]})

print(result["messages"][-1].content)

