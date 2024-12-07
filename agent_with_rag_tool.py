from llama_index.core import Settings
from llama_agents import (
    AgentService,
    AgentOrchestrator,
    ControlPlaneServer
)
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_agents.message_queues.apache_kafka import KafkaMessageQueue
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.ollama import Ollama
from retrievers.qdrant_ops import HybridQdrantOperations
import json

qdrant_ops = HybridQdrantOperations()
is_logging_enabled = True
# better managed from env
KAFKA_CONNECTION_URL = "localhost:9092"
llm = Ollama(base_url='http://localhost:11434', model='mistral:latest', temperature=0.8, request_timeout=300,
             system_prompt="You are an agent who consider the context passed "
                           "in, to answer any questions dont consider your prior "
                           "knowledge to answer and if you dont find the answer "
                           "please respond that you dont know.")
Settings.embed_model = OllamaEmbedding(base_url='http://localhost:11434', model_name='snowflake-arctic-embed:33m')


# create an agent
def get_startup_info(query: str) -> str:
    """Returns the information about startups."""
    if is_logging_enabled:
        print(f"Query from agent: {query}")
    resp = qdrant_ops.hybrid_search(text=query, top_k=5)
    if is_logging_enabled:
        print(f"Response from search: {resp}")
    return json.dumps(resp)


startup_info_tool = FunctionTool.from_defaults(fn=get_startup_info)
startup_tool_agent = ReActAgent.from_tools(tools=[startup_info_tool], llm=llm)
summarization_agent = ReActAgent.from_tools(tools=[], llm=llm)

message_queue = KafkaMessageQueue(url=KAFKA_CONNECTION_URL)

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