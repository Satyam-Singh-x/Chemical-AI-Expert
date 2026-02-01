# ====================== langgraph_database_backend.py ======================

from rag_chain import load_llm,build_rag_chain
from dotenv import load_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import StateGraph, START,END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

import requests
import os
import base64

# -------------------------------------------------------------------------



# -------------------------------------------------------------------------
# Initialize Hugging face llm
# -------------------------------------------------------------------------
llm =load_llm()





# -------------------------------------------------------------------------
# Define LangGraph State with image integration
# -------------------------------------------------------------------------
checkpointer = InMemorySaver()
rag=build_rag_chain()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


from langchain_core.messages import HumanMessage, AIMessage

def chat_node(state: ChatState):
    messages = state["messages"]

    # ✅ Extract the last human message (string)
    last_user_query = next(
        msg.content for msg in reversed(messages)
        if isinstance(msg, HumanMessage)
    )

    response_text = rag.invoke(last_user_query)

    return {
        "messages": [AIMessage(content=response_text)]
    }







graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

