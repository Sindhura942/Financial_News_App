import finnhub
import os
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv()


def get_finnhub_client():
    try:
        import streamlit as st
        api_key = st.secrets.get("FINNHUB_API_KEY", os.getenv("FINNHUB_API_KEY"))
    except:
        api_key = os.getenv("FINNHUB_API_KEY")
    return finnhub.Client(api_key=api_key)


@tool
def get_global_stock_quote(symbol: str) -> str:
    """Get real-time stock quote for global stocks."""
    try:
        client = get_finnhub_client()
        quote = client.quote(symbol)
        if quote.get('c', 0) == 0:
            return f"No data found for {symbol}"
        return f"**{symbol}**: ${quote['c']:.2f} ({quote['dp']:.2f}%)"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def get_company_news(symbol: str) -> str:
    """
    Fetch the latest company news for a given stock symbol.
    """
    try:
        client = get_finnhub_client()
        news = client.company_news(symbol, _from="2023-01-01", to="2023-01-07")
        if not news:
            return f"No news found for {symbol}."
        return "\n".join([f"- {item['headline']}" for item in news[:5]])
    except Exception as e:
        return f"Error fetching news for {symbol}: {str(e)}"


@tool
def get_market_status() -> str:
    """Get market status for major exchanges."""
    try:
        client = get_finnhub_client()
        status = client.market_status(exchange='US')
        return f"US Market: {'🟢 Open' if status.get('isOpen') else '🔴 Closed'}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool
def search_stock_symbol(query: str) -> str:
    """Search for stock symbols by company name."""
    try:
        client = get_finnhub_client()
        results = client.symbol_lookup(query)
        if not results.get('result'):
            return f"No symbols found for '{query}'"
        output = f"**Results for '{query}':**\n"
        for item in results['result'][:5]:
            output += f"- {item['symbol']}: {item['description']}\n"
        return output
    except Exception as e:
        return f"Error: {str(e)}"


def get_finnhub_tools():
    return [get_global_stock_quote, get_company_news, get_market_status, search_stock_symbol]