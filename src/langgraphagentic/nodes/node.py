import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

from langchain_openai import ChatOpenAI
from src.langgraphagentic.tools.stock_tools import get_stock_price, get_earnings_calendar, get_company_overview
from src.langgraphagentic.tools.search_tool import get_tools

# Get Tavily search tool and add Alpha Vantage tools
search_tools = get_tools()
tools = [get_stock_price, get_earnings_calendar, get_company_overview] + search_tools

# System prompt to improve accuracy
system_prompt = """You are a financial research assistant with access to accurate financial data tools.

IMPORTANT - Use the right tool for accurate data:
- For EARNINGS DATES: Use get_earnings_calendar (Alpha Vantage) - this is accurate
- For STOCK PRICES: Use get_stock_price (Alpha Vantage) - this is real-time
- For COMPANY INFO: Use get_company_overview (Alpha Vantage) - this is accurate
- For NEWS/GENERAL INFO: Use tavily_search - for recent news articles

Always prefer Alpha Vantage tools over web search for financial data like:
- Earnings dates
- Stock prices
- Company fundamentals
- Financial metrics

Only use web search for news articles and general information.
"""

llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools)

def chat_node(state):
    messages = state["messages"]
    # Add system prompt if not already present
    from langchain_core.messages import SystemMessage
    if not any(isinstance(m, SystemMessage) for m in messages):
        messages = [SystemMessage(content=system_prompt)] + list(messages)
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}