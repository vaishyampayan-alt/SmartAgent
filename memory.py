from langchain.memory import ConversationBufferWindowMemory


def build_memory() -> ConversationBufferWindowMemory:
    """
    Create and return a ConversationBufferWindowMemory instance.

    Keeps the last `k=10` conversation turns in memory, which is enough
    context for most multi-turn interactions without blowing the LLM context
    window.  `return_messages=True` ensures the history is returned as a list
    of BaseMessage objects (required by chat models).
    """
    return ConversationBufferWindowMemory(
        k=10,
        memory_key="chat_history",
        return_messages=True,
    )
