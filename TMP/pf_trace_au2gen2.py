import autogen
from pathlib import Path

parent_path = Path(__file__).resolve().parent.parent

config_list_gpt4 = autogen.config_list_from_dotenv(
    dotenv_file_path=f"{parent_path}/.env",
    model_api_key_map={
        "gpt-4o": {
            "api_key_env_var": "AZURE_OPENAI_API_KEY",
            "api_type": "azure",
            "api_version": "AZURE_OPENAI_API_VERSION",
            "base_url": "AZURE_OPENAI_ENDPOINT",
        },
    },
    filter_dict={
        "model": {
            "gpt-4o",
        }
    },
)
gpt4_config = {
    "cache_seed": 42,  # change the cache_seed for different trials
    "temperature": 0,
    "config_list": config_list_gpt4,
    # "timeout": 120,
}
print(gpt4_config)

# import logging
# logging.basicConfig(level=logging.DEBUG)
import os

os.environ["AUTOGEN_USE_DOCKER"] = "False"
u = autogen.UserProxyAgent(
    name="joke_listener",
    system_message="喜欢听笑话",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },
    human_input_mode="TERMINATE"
)
jkr = autogen.AssistantAgent(
    name="joke_teller",
    llm_config=gpt4_config,
    system_message="""能根据你的需要编笑话.然后讲给 joke_listener 和 joke_critic 听.""",
)
jkrcritic = autogen.AssistantAgent(
    name="joke_critic",
    llm_config=gpt4_config,
    system_message="""评估 joke_teller 讲的笑话好不好笑.""",
)
jk_grp = autogen.GroupChat(
    agents=[u, jkr, jkrcritic], messages=[], max_round=9
)
manager = autogen.GroupChatManager(groupchat=jk_grp, llm_config=gpt4_config)

from promptflow.tracing import start_trace
# start a trace session, and print a url for user to check trace
# traces will be collected into below collection name
start_trace(collection="autogen_joke2")

from opentelemetry import trace
import json
tracer = trace.get_tracer("mytracer2")
# Create a root span
with tracer.start_as_current_span("autogen") as span:
    message = """讲一个熊猫相关的笑话"""
    u.initiate_chat(
        manager,
        message=message,
        clear_history=True,
    )
    span.set_attribute("custom", "custom attribute value")
    # recommend to store inputs and outputs as events
    span.add_event(
        "promptflow.function.inputs", {"payload": json.dumps(dict(message=message))}
    )
    span.add_event(
        "promptflow.function.output", {"payload": json.dumps(u.last_message())}
    )
