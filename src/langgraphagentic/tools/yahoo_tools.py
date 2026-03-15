import yfinance as yf
from langchain_core.tools import tool


@tool
def get_stock_info(symbol: str) -> str:
    """
    Get detailed stock information including price, market cap, P/E ratio, dividends, etc.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT', 'RELIANCE.NS', 'TCS.NS')
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        if not info or info.get('regularMarketPrice') is None:
            return f"No data found for symbol: {symbol}"
        
        return f"""
**{info.get('longName', symbol)} ({symbol})**

💰 **Price Information:**
- Current Price: ${info.get('regularMarketPrice', 'N/A')}
- Previous Close: ${info.get('previousClose', 'N/A')}
- Day High: ${info.get('dayHigh', 'N/A')}
- Day Low: ${info.get('dayLow', 'N/A')}
- 52 Week High: ${info.get('fiftyTwoWeekHigh', 'N/A')}
- 52 Week Low: ${info.get('fiftyTwoWeekLow', 'N/A')}

📊 **Key Metrics:**
- Market Cap: ${info.get('marketCap', 'N/A'):,}
- P/E Ratio: {info.get('trailingPE', 'N/A')}
- EPS: ${info.get('trailingEps', 'N/A')}
- Dividend Yield: {info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 'N/A'}%

🏢 **Company Info:**
- Sector: {info.get('sector', 'N/A')}
- Industry: {info.get('industry', 'N/A')}
- Country: {info.get('country', 'N/A')}
- Employees: {info.get('fullTimeEmployees', 'N/A'):,}
"""
    except Exception as e:
        return f"Error fetching data for {symbol}: {str(e)}"


@tool
def get_stock_history(symbol: str, period: str = "1mo") -> str:
    """
    Get historical stock prices.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'GOOGL')
        period: Time period - '1d', '5d', '1mo', '3mo', '6mo', '1y', '5y', 'max'
    """
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(period=period)
        
        if hist.empty:
            return f"No historical data found for {symbol}"
        
        result = f"**{symbol} - Last {period} Price History:**\n\n"
        result += "| Date | Open | High | Low | Close | Volume |\n"
        result += "|------|------|------|-----|-------|--------|\n"
        
        # Show last 10 entries
        for date, row in hist.tail(10).iterrows():
            result += f"| {date.strftime('%Y-%m-%d')} | ${row['Open']:.2f} | ${row['High']:.2f} | ${row['Low']:.2f} | ${row['Close']:.2f} | {int(row['Volume']):,} |\n"
        
        return result
    except Exception as e:
        return f"Error fetching history for {symbol}: {str(e)}"


@tool
def get_analyst_recommendations(symbol: str) -> str:
    """
    Get analyst recommendations (buy, hold, sell) for a stock.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'TSLA')
    """
    try:
        stock = yf.Ticker(symbol)
        rec = stock.recommendations
        
        if rec is None or rec.empty:
            return f"No analyst recommendations found for {symbol}"
        
        result = f"**Analyst Recommendations for {symbol}:**\n\n"
        
        # Get latest recommendations
        latest = rec.tail(5)
        for date, row in latest.iterrows():
            result += f"- **{row.get('Firm', 'Unknown')}**: {row.get('To Grade', 'N/A')} ({date.strftime('%Y-%m-%d')})\n"
        
        return result
    except Exception as e:
        return f"Error fetching recommendations for {symbol}: {str(e)}"


@tool
def get_financials(symbol: str) -> str:
    """
    Get key financial data (revenue, profit, etc.) for a company.
    
    Args:
        symbol: Stock symbol (e.g., 'AAPL', 'MSFT')
    """
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        financials = stock.financials
        
        if financials is None or financials.empty:
            return f"No financial data found for {symbol}"
        
        result = f"**{info.get('longName', symbol)} Financials:**\n\n"
        
        # Key financial metrics from info
        result += f"💵 **Revenue (TTM):** ${info.get('totalRevenue', 0):,}\n"
        result += f"💰 **Gross Profit:** ${info.get('grossProfits', 0):,}\n"
        result += f"📈 **Operating Margin:** {info.get('operatingMargins', 0) * 100:.2f}%\n"
        result += f"📊 **Profit Margin:** {info.get('profitMargins', 0) * 100:.2f}%\n"
        result += f"💳 **Total Debt:** ${info.get('totalDebt', 0):,}\n"
        result += f"💵 **Total Cash:** ${info.get('totalCash', 0):,}\n"
        result += f"📉 **Debt to Equity:** {info.get('debtToEquity', 'N/A')}\n"
        
        return result
    except Exception as e:
        return f"Error fetching financials for {symbol}: {str(e)}"


@tool
def compare_stocks(symbols: str) -> str:
    """
    Compare multiple stocks side by side.
    
    Args:
        symbols: Comma-separated stock symbols (e.g., 'AAPL,MSFT,GOOGL')
    """
    try:
        symbol_list = [s.strip() for s in symbols.split(',')]
        
        result = "**Stock Comparison:**\n\n"
        result += "| Metric | " + " | ".join(symbol_list) + " |\n"
        result += "|--------|" + "|".join(["------" for _ in symbol_list]) + "|\n"
        
        data = {}
        for symbol in symbol_list:
            stock = yf.Ticker(symbol)
            data[symbol] = stock.info
        
        metrics = [
            ('Price', 'regularMarketPrice', '$'),
            ('Market Cap', 'marketCap', '$'),
            ('P/E Ratio', 'trailingPE', ''),
            ('Div Yield', 'dividendYield', '%'),
        ]
        
        for metric_name, key, prefix in metrics:
            row = f"| {metric_name} |"
            for symbol in symbol_list:
                val = data[symbol].get(key, 'N/A')
                if val != 'N/A' and val is not None:
                    if prefix == '$':
                        row += f" {prefix}{val:,.2f} |"
                    elif prefix == '%':
                        row += f" {val * 100:.2f}{prefix} |"
                    else:
                        row += f" {val:.2f} |"
                else:
                    row += " N/A |"
            result += row + "\n"
        
        return result
    except Exception as e:
        return f"Error comparing stocks: {str(e)}"


def get_yahoo_tools():
    """Return all Yahoo Finance tools"""
    return [
        get_stock_info,
        get_stock_history,
        get_analyst_recommendations,
        get_financials,
        compare_stocks
    ]