from langchain_openai import ChatOpenAI
from src.langgraphagentic.state.state import State
from src.langgraphagentic.tools.stock_tools import get_stock_price, get_earnings_calendar, get_company_overview
from src.langgraphagentic.tools.search_tool import get_tools
from src.langgraphagentic.tools.finnhub_tools import get_finnhub_tools
from src.langgraphagentic.tools.yahoo_tools import get_yahoo_tools
from dotenv import load_dotenv
from pathlib import Path
import os

# Load environment variables
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get OpenAI API key from environment or Streamlit secrets
def get_openai_api_key():
    try:
        import streamlit as st
        return st.secrets.get("OPENAI_API_KEY", os.getenv("OPENAI_API_KEY"))
    except:
        return os.getenv("OPENAI_API_KEY")

# Combine all tools
search_tools = get_tools()
finnhub_tools = get_finnhub_tools()
yahoo_tools = get_yahoo_tools()
tools = [get_stock_price, get_earnings_calendar, get_company_overview] + search_tools + finnhub_tools + yahoo_tools

llm = ChatOpenAI(model="gpt-4o-mini", api_key=get_openai_api_key())
llm_with_tools = llm.bind_tools(tools)

# System prompt for accurate financial data
SYSTEM_PROMPT = """You are a helpful financial research assistant with access to multiple data sources:

📊 **Alpha Vantage** (US Stocks):
- get_stock_price: Real-time US stock prices
- get_earnings_calendar: Earnings announcement dates  
- get_company_overview: Company information

🌍 **Finnhub** (Global Stocks):
- get_global_stock_quote: Real-time global stock quotes
- get_company_news: Latest company news
- get_market_status: Check if markets are open
- search_stock_symbol: Find stock symbols

📈 **Yahoo Finance** (Detailed Analysis):
- get_stock_info: Comprehensive stock data (price, P/E, dividends, etc.)
- get_stock_history: Historical price data
- get_analyst_recommendations: Buy/Hold/Sell ratings
- get_financials: Revenue, profit, margins
- compare_stocks: Compare multiple stocks side by side

🔍 **Tavily Search**: Financial news and research

**Stock Symbol Formats:**
- US: AAPL, MSFT, GOOGL
- India NSE: TCS.NS, RELIANCE.NS
- India BSE: TCS.BO, RELIANCE.BO  
- Germany: BMW.DE, SAP.DE
- UK: HSBA.L, BP.L

Always use the most appropriate tool for the user's question."""

def chat_node(state: State):
    messages = state["messages"]
    from langchain_core.messages import SystemMessage
    messages_with_system = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages_with_system)
    return {"messages": [response]}