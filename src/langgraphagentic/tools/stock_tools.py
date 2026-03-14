import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
import requests

# Load .env from project root (for local development)
env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(env_path)

def get_api_key(key_name):
    """Get API key from environment or Streamlit secrets"""
    api_key = os.getenv(key_name)
    if api_key:
        return api_key
    # Try Streamlit secrets (for cloud deployment)
    try:
        import streamlit as st
        return st.secrets.get(key_name)
    except:
        return None

@tool
def get_stock_price(symbol: str) -> dict:
    """Get the current stock price for a given symbol like AAPL, MSFT, SCHW, etc."""
    api_key = get_api_key("ALPHAVANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    r = requests.get(url)
    return r.json()

@tool
def get_earnings_calendar(symbol: str) -> dict:
    """
    Get the earnings announcement date for a specific company.
    Use this for accurate earnings dates instead of web search.
    Example: get_earnings_calendar("SCHW") for Charles Schwab earnings date.
    """
    api_key = get_api_key("ALPHAVANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={symbol}&horizon=3month&apikey={api_key}"
    r = requests.get(url)
    
    # Parse CSV response
    lines = r.text.strip().split('\n')
    if len(lines) > 1:
        headers = lines[0].split(',')
        data = lines[1].split(',')
        result = dict(zip(headers, data))
        return {
            "symbol": result.get("symbol", symbol),
            "earnings_date": result.get("reportDate", "Not available"),
            "estimate_eps": result.get("estimate", "N/A"),
            "currency": result.get("currency", "USD")
        }
    return {"error": "No earnings data found", "symbol": symbol}

@tool
def get_company_overview(symbol: str) -> dict:
    """
    Get company overview including description, sector, industry, market cap, 
    P/E ratio, dividend yield, 52-week high/low, and earnings dates.
    """
    api_key = get_api_key("ALPHAVANTAGE_API_KEY")
    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}"
    r = requests.get(url)
    data = r.json()
    
    # Return relevant fields
    return {
        "symbol": data.get("Symbol"),
        "name": data.get("Name"),
        "description": data.get("Description", "")[:300] + "...",
        "sector": data.get("Sector"),
        "industry": data.get("Industry"),
        "market_cap": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "dividend_yield": data.get("DividendYield"),
        "52_week_high": data.get("52WeekHigh"),
        "52_week_low": data.get("52WeekLow"),
        "earnings_date": data.get("LatestQuarter")
    }
