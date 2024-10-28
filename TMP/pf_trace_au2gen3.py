"""
这个时不时无法trace,不知道为何
"""
import autogen

# please ensure you have a json config file
env_or_file = "OAI_CONFIG_LIST.json"

# filters the configs by models (you can filter by other keys as well). Only the gpt-4 models are kept in the list based on the filter condition.

# gpt4
# config_list = autogen.config_list_from_json(
#     env_or_file,
#     filter_dict={
#         "model": ["gpt-4", "gpt-4-0314", "gpt4", "gpt-4-32k", "gpt-4-32k-0314", "gpt-4-32k-v0314"],
#     },
# )

# gpt35
config_list = autogen.config_list_from_json(
    env_or_file,
    filter_dict={
        "model": {
            # "gpt-35-turbo",
            # "gpt-3.5-turbo",
            # "gpt-3.5-turbo-16k",
            # "gpt-3.5-turbo-0301",
            # "chatgpt-35-turbo-0301",
            # "gpt-35-turbo-v0301",
            "gpt-4o"
        },
    },
)






import os

os.environ["AUTOGEN_USE_DOCKER"] = "False"

llm_config = {"config_list": config_list, "cache_seed": 42}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="喜欢听笑话",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="TERMINATE",
)
coder = autogen.AssistantAgent(
    name="joke_teller",
    llm_config=llm_config,
    system_message="""能根据你的需要编笑话.然后讲给 joke_listener 和 joke_critic 听.""",
)
pm = autogen.AssistantAgent(
    name="joke_critic",
    system_message="""评估 joke_teller 讲的笑话好不好笑.""",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)





from promptflow.tracing import start_trace

# start a trace session, and print a url for user to check trace
# traces will be collected into below collection name
start_trace(collection="autogen-groupchat6")





from opentelemetry import trace
import json


tracer = trace.get_tracer("my_tracer6")
# Create a root span
with tracer.start_as_current_span("autogen6") as span:
    message = """讲一个熊猫相关的笑话"""
    user_proxy.initiate_chat(
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
        "promptflow.function.output", {"payload": json.dumps(user_proxy.last_message())}
    )
# type exit to terminate the chat





