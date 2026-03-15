from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from src.langgraphagentic.nodes.node import chat_node
from src.langgraphagentic.tools.stock_tools import get_stock_price, get_earnings_calendar, get_company_overview
from src.langgraphagentic.tools.search_tool import get_tools
from src.langgraphagentic.state.state import State as ChatState
from src.langgraphagentic.graph.graph_builder import chatbot

# Get Tavily search tool and add Alpha Vantage tools
search_tools = get_tools()
tools = [get_stock_price, get_earnings_calendar, get_company_overview] + search_tools

graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", ToolNode(tools))

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

# Add memory checkpointer for stateful conversations
memory = MemorySaver()
chatbot = graph.compile(checkpointer=memory)
