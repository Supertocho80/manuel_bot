# 🤖 Manuel Broker Bot

English | [Español](README.es.md)

**Manuel Broker** is a financial assistant for Telegram written in Python. It combines real-time market data (Yahoo Finance) with a **local AI model** (Ollama + Phi-3 Mini) to give quotes, asset comparisons, trend analysis and simple financial explanations — without sending anything to a cloud AI.

## ✨ Features

* **💰 Real-time prices:** stocks (Apple, Inditex…), indices (S&P 500, IBEX 35, Nasdaq), crypto (Bitcoin, Ethereum…), commodities (gold, silver) and EUR/USD.
* **🥊 Asset comparison:** puts two assets head to head on relative daily performance.
* **🔮 Hybrid trend analysis:** a math-based Bullish / Bearish / Sideways verdict from real data, plus a short AI comment.
* **📖 AI financial dictionary:** explains financial terms in plain language and rejects non-financial topics.
* **🌱 Passive-investing guide (Bogleheads):** diversification and long-term investing basics.
* **🧠 Robustness:**
  * **Alias map:** dozens of everyday names mapped to tickers (e.g. "Manzana" (Spanish for apple) → `AAPL`, "Zara" → `ITX.MC`, "Oro" → `GC=F`).
  * **Typo handling:** if a ticker is not recognised, the AI suggests one and the bot asks for confirmation with inline buttons.
  * **In-memory cache:** market data for 60 s and AI text for 300 s, to save calls to Yahoo and to the model.
  * **Safe output:** `html.escape` on everything sent to the chat; answers wrapped in `<<< >>>` and temperature 0.0 to reduce hallucinations.

## 🛠️ Tech stack

| Area | Technology |
|---|---|
| Language | Python 3.10+ |
| Bot framework | `python-telegram-bot` 22 (async, `Application`, command and callback handlers) |
| Market data | `yfinance` |
| Local AI | Ollama HTTP API (`http://localhost:11434/api/generate`), model `phi3:mini` |
| Config | `python-dotenv` (`.env`) |

## 🏗️ Project structure

```
manuel_bot/
├── main.py            # Entry point: builds the Telegram Application and registers the handlers
├── config.py          # Token from .env, Ollama URL and model, cache TTLs, alias → ticker map
├── cerebro.py         # Core logic: Ollama calls, Yahoo data, cache, ticker guessing,
│                      # financial-topic filter, confirmation flow and message formatting
├── comandos/          # One module per command
│   ├── start.py       # /start + interactive menu
│   ├── precio.py      # /precio
│   ├── comparar.py    # /comparar
│   ├── tendencia.py   # /tendencia
│   ├── explica.py     # /explica
│   ├── invertir.py    # /como_invertir
│   ├── ayuda.py       # /ayuda
│   └── callbacks.py   # Inline-button handler (menu and confirmations)
└── requirements.txt
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Supertocho80/manuel_bot.git
cd manuel_bot
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Install Ollama and the model

```bash
ollama pull phi3:mini
ollama serve                    # if it is not already running
```

### 4. Environment variables

Create a `.env` file in the project root (keep it out of Git):

```env
MANUELBROKER_TOKEN=YOUR_TOKEN_FROM_BOTFATHER
```

### 5. Run the bot

```bash
python main.py
```

## 🎮 Commands

The bot talks in Spanish, so command names are in Spanish.

| Command | Example | Description |
| --- | --- | --- |
| `/start` | `/start` | Starts the bot and shows the interactive menu. |
| `/precio` | `/precio Apple` | Current price and percentage change. |
| `/comparar` | `/comparar BTC Oro` | Compares the daily performance of two assets ("Oro" = gold). |
| `/explica` | `/explica Warrants` | AI definition of a financial term. |
| `/tendencia` | `/tendencia Tesla` | Bullish / bearish / sideways trend + AI comment. |
| `/como_invertir` | `/como_invertir` | Basic guide to the Bogleheads philosophy. |
| `/ayuda` | `/ayuda` | Quick list of commands. |

## ⚠️ Disclaimer

Educational project. Nothing the bot says is investment advice.

---

Made with 🐍 Python, ❤️ and coffee.
