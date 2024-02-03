from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from langchain.agents.agent_types import AgentType
from langchain.agents import create_sql_agent
from langchain.memory import ConversationBufferMemory


from utils import get_chat_openai
from tools.functions_tools import sql_agent_tools
from database.sql_db_langchain import db
from .agent_constants import CUSTOM_SUFFIX


def get_sql_toolkit(tool_llm_name: str):
    """
    Get the SQL toolkit for a given tool LLM name.

    Parameters:
        tool_llm_name (str): The name of the tool LLM.

    Returns:
        SQLDatabaseToolkit: The SQL toolkit object.
    """
    llm_tool = get_chat_openai(model_name=tool_llm_name)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm_tool)
    return toolkit


def get_agent_llm(agent_llm_name: str):
    """
    Retrieves the LLM agent with the specified name.

    Parameters:
        agent_llm_name (str): The name of the LLN agent.

    Returns:
        llm_agent: The LLM agent object.
    """
    llm_agent = get_chat_openai(model_name=agent_llm_name)
    return llm_agent


def create_agent(
    tool_llm_name: str = "gpt-4-1106-preview",
    agent_llm_name: str = "gpt-4-1106-preview",
):
    """
    Creates a SQL agent using the specified tool and agent LLM names.

    Args:
        tool_llm_name (str, optional): The name of the SQL toolkit LLM. Defaults to "gpt-4-1106-preview".
        agent_llm_name (str, optional): The name of the agent LLM. Defaults to "gpt-4-1106-preview".

    Returns:
        agent: The created SQL agent.
    """

    agent_tools = sql_agent_tools()
    llm_agent = get_agent_llm(agent_llm_name)
    toolkit = get_sql_toolkit(tool_llm_name)
    memory = ConversationBufferMemory(memory_key="history", input_key="input")

    agent = create_sql_agent(
        llm=llm_agent,
        toolkit=toolkit,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        input_variables=["input", "agent_scratchpad", "history"],
        suffix=CUSTOM_SUFFIX,
        agent_executor_kwargs={"memory": memory},
        extra_tools=agent_tools,
        verbose=True,
    )
    return agent
