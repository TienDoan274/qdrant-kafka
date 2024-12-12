from llama_index.llms.ollama import Ollama
from llama_index.llms.openai import OpenAI

llm = Ollama(base_url='http://localhost:11434', model='mistral:latest', temperature=0.8, request_timeout=300,
             system_prompt="You are an agent who consider the context passed "
                           "in, to answer any questions dont consider your prior "
                           "knowledge to answer and if you dont find the answer "
                           "please respond that you dont know.")

print(llm.complete('hello'))