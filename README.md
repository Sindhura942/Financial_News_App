# 📊 AGENTIC: Financial Research Assistant

An AI-powered financial research chatbot built with LangGraph, OpenAI, and Streamlit. Get real-time stock prices, earnings dates, company information, and financial news in one place.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic-green)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)

## ✨ Features

- **📈 Real-time Stock Prices** - Get current stock prices using Alpha Vantage API
- **📅 Earnings Calendar** - Accurate earnings announcement dates
- **🏢 Company Overview** - Sector, industry, market cap, P/E ratio, and more
- **📰 Financial News Search** - Latest news using Tavily Search
- **💬 Conversational AI** - Natural language chat interface
- **🧠 Stateful Conversations** - Remembers context within a session

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| LLM Framework | LangGraph + LangChain |
| Language Model | OpenAI GPT-4o-mini |
| Stock Data | Alpha Vantage API |
| News Search | Tavily API |
| UI | Streamlit |
| State Management | LangGraph MemorySaver |

## 📁 Project Structure

```
Financial_News_App/
├── app.py                          # Streamlit entry point
├── .env                            # API keys (not committed)
├── .gitignore
├── requirements.txt
├── README.md
├── DEVELOPMENT_NOTES.md            # Development documentation
├── ERROR_LOG.md                    # Error tracking & solutions
└── src/
    └── langgraphagentic/
        ├── __init__.py
        ├── main.py                 # Alternative entry point
        ├── graph/
        │   ├── __init__.py
        │   └── graph_builder.py    # LangGraph workflow
        ├── nodes/
        │   ├── __init__.py
        │   └── node.py             # Chat node with LLM
        ├── state/
        │   ├── __init__.py
        │   └── state.py            # State definition
        ├── tools/
        │   ├── __init__.py
        │   ├── stock_tools.py      # Alpha Vantage tools
        │   └── search_tool.py      # Tavily search tool
        └── ui/
            └── streamlite/
                ├── uiconfigfile.ini
                ├── uiconfigfile.py
                ├── loadui.py
                └── display_result.py
```

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Financial_News_App.git
cd Financial_News_App
```

### 2. Create Virtual Environment
```bash
# Using conda (recommended)
conda create --prefix ./myvenv python=3.11
conda activate ./myvenv

# Or using venv
python -m venv myvenv
source myvenv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
ALPHAVANTAGE_API_KEY=your_alphavantage_api_key
TAVILY_API_KEY=your_tavily_api_key
```

**Get your API keys:**
- OpenAI: https://platform.openai.com/api-keys
- Alpha Vantage: https://www.alphavantage.co/support/#api-key (Free)
- Tavily: https://tavily.com/ (Free tier available)

### 5. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 💬 Example Queries

| Query | Tool Used |
|-------|-----------|
| "What's the stock price of AAPL?" | `get_stock_price` |
| "When does Schwab announce earnings?" | `get_earnings_calendar` |
| "Tell me about Microsoft as a company" | `get_company_overview` |
| "What's the latest news about Tesla?" | `tavily_search` |
| "Compare Apple and Google stock prices" | `get_stock_price` (multiple) |

## 🔧 Available Tools

### 1. Stock Price (`get_stock_price`)
```
Input: Stock symbol (e.g., "AAPL", "MSFT", "SCHW")
Output: Current price, open, high, low, volume, change %
```

### 2. Earnings Calendar (`get_earnings_calendar`)
```
Input: Stock symbol
Output: Next earnings date, estimated EPS
```

### 3. Company Overview (`get_company_overview`)
```
Input: Stock symbol
Output: Name, sector, industry, market cap, P/E ratio, 52-week high/low
```

### 4. Financial News Search (`tavily_search`)
```
Input: Search query
Output: Recent news articles with titles, URLs, and summaries
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Streamlit UI                         │
└─────────────────────────┬───────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────┐
│                   LangGraph Agent                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │  Chat Node  │───▶│   Router    │───▶│ Tool Node   │ │
│  │  (GPT-4o)   │    │ (Condition) │    │             │ │
│  └─────────────┘    └─────────────┘    └──────┬──────┘ │
│                                               │        │
│         ┌────────────────────────────────────┘        │
│         ▼                                              │
│  ┌─────────────────────────────────────────────────┐  │
│  │                    Tools                         │  │
│  │  ┌───────────┐ ┌───────────┐ ┌───────────────┐  │  │
│  │  │  Stock    │ │ Earnings  │ │   Company     │  │  │
│  │  │  Price    │ │ Calendar  │ │   Overview    │  │  │
│  │  └─────┬─────┘ └─────┬─────┘ └───────┬───────┘  │  │
│  │        └─────────────┼───────────────┘          │  │
│  │                      ▼                          │  │
│  │              Alpha Vantage API                  │  │
│  │                                                 │  │
│  │  ┌───────────────────────────────────────────┐ │  │
│  │  │            Tavily Search                  │ │  │
│  │  └───────────────────────────────────────────┘ │  │
│  └─────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────┘
```

## 📝 State Management

The app uses LangGraph's `MemorySaver` for stateful conversations:

```python
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()
chatbot = graph.compile(checkpointer=memory)
```

This enables:
- Context-aware follow-up questions
- Conversation history within a session
- Reference to previous queries

## ⚠️ Limitations

- **Alpha Vantage Free Tier**: 25 requests/day, 5 requests/minute
- **In-Memory State**: Conversation history is lost on app restart
- **Single User**: No multi-user session management

## 🔮 Future Enhancements

- [ ] Add PostgreSQL for persistent state
- [ ] Multi-user session support
- [ ] Stock price charts and visualizations
- [ ] Portfolio tracking
- [ ] Price alerts
- [ ] Historical data analysis

## 📄 License

MIT License

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Contact

Your Name - mulpurisindhura942@gmail.com

Project Link: https://github.com/yourusername/Financial_News_App
