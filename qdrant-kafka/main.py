from llama_agents import LocalLauncher
from agent_with_rag_tool import startup_service, summarization_service, control_plane, message_queue

# launch it
launcher = LocalLauncher(
    [startup_service, summarization_service],
    control_plane,
    message_queue,
)

while True:
    input_query = input("Query (type 'bye' or 'exit' to quit the program ):")
    if input_query.lower() == 'bye' or input_query.lower() == 'exit':
        break
    result = launcher.launch_single(initial_task=input_query)
    print(f"Result: {result}")