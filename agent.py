"""
agent.py — Assembles and returns the SmartAgent AgentExecutor.

Exported interface:
    build_agent() -> AgentExecutor
"""

import os
from dotenv import load_dotenv

from langchain import hub
from langchain.agents import create_react_agent, AgentExecutor
from langchain_groq import ChatGroq

from tools import web_search, write_file, read_file, calculator, summarize_text
from memory import build_memory

# ---------------------------------------------------------------------------
# Load environment variables from .env (no-op if already loaded)
# ---------------------------------------------------------------------------
load_dotenv()


def build_agent() -> AgentExecutor:
    """
    Build and return a fully configured SmartAgent AgentExecutor.

    Components
    ----------
    - LLM     : Groq ``llama3-70b-8192`` loaded via GROQ_API_KEY
    - Prompt  : ``hwchase17/react-chat`` from LangChain Hub
    - Tools   : web_search, write_file, read_file, calculator, summarize_text
    - Memory  : ConversationBufferWindowMemory (k=10)
    - Executor: verbose, max_iterations=10, handle_parsing_errors=True
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GROQ_API_KEY is not set. "
            "Copy .env.example to .env and add your key."
        )

    # ------------------------------------------------------------------
    # 1. LLM
    # ------------------------------------------------------------------
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0,
    )

    # ------------------------------------------------------------------
    # 2. Tools
    # ------------------------------------------------------------------
    tools = [
        web_search,
        write_file,
        read_file,
        calculator,
        summarize_text,
    ]

    # ------------------------------------------------------------------
    # 3. Prompt  (ReAct chat variant from LangChain Hub)
    # ------------------------------------------------------------------
    prompt = hub.pull("hwchase17/react-chat")

    # ------------------------------------------------------------------
    # 4. Memory
    # ------------------------------------------------------------------
    memory = build_memory()

    # ------------------------------------------------------------------
    # 5. Assemble agent + executor
    # ------------------------------------------------------------------
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True,
    )

    return executor
