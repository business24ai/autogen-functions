# Import things that are needed generically
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type
import math
import os


from autogen import AssistantAgent, UserProxyAgent, config_list_from_json

from get_stock import get_stock_price

import openai

import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST") 

termination = ' If "Thank you" or "Terminate" or "Goodbye" are said in conversation, then respond with "TERMINATE as your last message and finish the conversation immediately.'

assistent = AssistantAgent(
    "assistant",
    system_message="You are a Hedge Fund Manager running an AI Hedge Fond. Do not show any appreciation in your responses. Keep it as short as possible. Only use the functions you have been provided with. Reply TERMINATE when the task is done.",
    llm_config={
        "config_list": config_list,
        "request_timeout": 120,
        "functions": [
            {
                "name": "get_stock_price",
                "description": "Get the ticker of a stock and returns the latest closing price",
                "parameters":{
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "The ticker symbol od the stock",
                        },
                    },
                    "required": ["ticker"],
                },
            }
        ]
    }
)

user_proxy = UserProxyAgent(
    "user_proxy",
    code_execution_config={"work_dir": "coding"},
    is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    system_message='Do not show any appreciation in your responses. Keep it as short as possible.',
    function_map={"get_stock_price": get_stock_price}
)


user_proxy.initiate_chat(assistent, message="What is the latest price of Microsoft" + termination)




