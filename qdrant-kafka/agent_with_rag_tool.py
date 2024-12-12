from llama_index.core import Settings
from llama_agents import (
    AgentService,
    AgentOrchestrator,
    ControlPlaneServer,
    SimpleMessageQueue
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_agents.message_queues.apache_kafka import KafkaMessageQueue
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from retrievers.qdrant_ops import HybridQdrantOperations
import json
from llama_index.llms.openai import OpenAI

qdrant_ops = HybridQdrantOperations()
is_logging_enabled = True
# better managed from env
KAFKA_CONNECTION_URL = "localhost:9092"
# llm = Ollama(base_url='http://localhost:11434', model='llama3.1:latest', temperature=0.8, request_timeout=300,
#              system_prompt="You are an agent who consider the context passed "
#                            "in, to answer any questions dont consider your prior "
#                            "knowledge to answer and if you dont find the answer "
#                            "please respond that you dont know.")
Settings.embed_model = OllamaEmbedding(base_url='http://localhost:11434', model_name='snowflake-arctic-embed:33m')


# create an agent
def get_startup_info(query: str) -> str:
    """Returns the information about startups."""
    if is_logging_enabled:
        print(f"Query from agent: {query}")
    resp = qdrant_ops.search(text=query, limit=1)[0]['description']
    if is_logging_enabled:
        print(f"Response from search: {resp}")
    return (resp)


startup_info_tool = FunctionTool.from_defaults(fn=get_startup_info)
startup_tool_agent = ReActAgent.from_tools(tools=[startup_info_tool], llm=llm)
summarization_agent = ReActAgent.from_tools(tools=[], llm=llm)

message_queue = KafkaMessageQueue(url=KAFKA_CONNECTION_URL)
# message_queue = SimpleMessageQueue(port=8000)

control_plane = ControlPlaneServer(
    message_queue=message_queue,
    orchestrator=AgentOrchestrator(llm=llm),
    port=8001,
)
startup_service = AgentService(
    agent=startup_tool_agent,
    message_queue=message_queue,
    description="Useful for getting the information about startups.",
    service_name="info_extract_agent",
    port=8002,
)
summarization_service = AgentService(
    agent=summarization_agent,
    message_queue=message_queue,
    description="Useful for consolidating or summarizing the information.",
    service_name="info_summarization_agent",
    port=8003,
)

from llama_agents import LocalLauncher
import nest_asyncio


launcher = LocalLauncher(
    [startup_service, summarization_service],
    control_plane,
    message_queue,
)
result = launcher.launch_single("What are startups in San Francisco ?")

print(f"Result: {result}")