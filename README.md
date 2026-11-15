# 🤖 Manuel Broker Bot

English | [Español](README.es.md)

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22-229ED9.svg?logo=telegram&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-market%20data-00A86B.svg)
![Ollama](https://img.shields.io/badge/Ollama-local%20AI-000000.svg)
![Phi--3](https://img.shields.io/badge/Model-phi3%3Amini-8B5CF6.svg)
![dotenv](https://img.shields.io/badge/dotenv-config-ECD53F.svg)

> **Status: educational project.** A Telegram financial assistant that keeps market data and AI inference on your machine — Yahoo Finance for quotes, Ollama for explanations.

**Manuel Broker** is a Python bot for Telegram. It combines real-time market data with a **local AI model** (Ollama + Phi-3 Mini) to deliver quotes, comparisons, trend analysis and plain-language financial definitions without sending user prompts to a cloud LLM.

---

## 🚀 Architecture and Tech Stack

The codebase is **modular**: `main.py` wires the Telegram `Application`, each command lives under `comandos/`, and shared logic (Yahoo, Ollama, cache, aliases, confirmations) sits in `cerebro.py`.

| Layer | Technology |
|------|------------|
| **Runtime** | Python 3.10+ |
| **Bot framework** | `python-telegram-bot` 22 — async `Application`, command and callback handlers |
| **Market data** | `yfinance` (OHLC, daily change) |
| **Local AI** | Ollama HTTP API (`http://localhost:11434/api/generate`), model `phi3:mini` |
| **Configuration** | `python-dotenv` — `MANUELBROKER_TOKEN` in `.env` |
| **Caching** | In-memory dict in `cerebro.py` — market data 60 s, AI text 300 s |

```
┌──────────────┐   Telegram API    ┌─────────────────────────────────────┐
│  User chat   │ ◄────────────────► │  main.py + comandos/ (handlers)     │
└──────────────┘                   └──────────────────┬──────────────────┘
                                                    │
                         ┌──────────────────────────▼──────────────────────────┐
                         │  cerebro.py — aliases, cache, confirmations, format │
                         └─────────────┬───────────────────────┬─────────────┘
                                       │                       │
                            ┌──────────▼──────────┐   ┌──────────▼──────────┐
                            │  Yahoo (yfinance)   │   │  Ollama (phi3:mini) │
                            └─────────────────────┘   └─────────────────────┘
```

---

## ✨ Key Features

| Feature | What it does |
|---------|----------------|
| **Real-time prices** | Stocks, indices, crypto, commodities and EUR/USD via alias map (e.g. "Manzana" → `AAPL`, "Oro" → `GC=F`). |
| **Asset comparison** | Head-to-head daily performance for two tickers or aliases. |
| **Hybrid trend** | Math-based Bullish / Bearish / Sideways from price action, plus a short AI comment. |
| **Financial dictionary** | `/explica` defines terms with AI; non-financial topics are rejected. |
| **Passive investing guide** | `/como_invertir` — Bogleheads-style basics. |
| **Typo recovery** | Unknown tickers trigger an AI suggestion and inline confirmation buttons. |
| **Safe chat output** | `html.escape` on bot messages; AI replies use `<<< >>>` wrappers and temperature `0.0`. |

---

## ⚙️ Prerequisites

| Tool | Notes |
|------|--------|
| **Python** | 3.10 or newer |
| **Ollama** | Running locally; pull model `phi3:mini` |
| **Telegram bot token** | From [@BotFather](https://t.me/BotFather) |
| **Internet** | For Telegram and Yahoo Finance (not for cloud AI) |

---

## 📦 Installation and Startup

### Step 0 · Environment variables (required)

Create **`.env` in the repository root** (listed in `.gitignore`):

```env
MANUELBROKER_TOKEN=YOUR_TOKEN_FROM_BOTFATHER
```

### Step 1 · Clone the repository

```bash
git clone https://github.com/Supertocho80/manuel_bot.git
cd manuel_bot
```

### Step 2 · Virtual environment and dependencies

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Step 3 · Ollama and the model

```bash
ollama pull phi3:mini
ollama serve                    # if not already running
```

### Step 4 · Run the bot

```bash
python main.py
```

---

## 📖 Usage Guide

The bot speaks **Spanish** in the chat; command names are Spanish.

### Commands

| Command | Example | Description |
| --- | --- | --- |
| `/start` | `/start` | Starts the bot and shows the interactive menu. |
| `/precio` | `/precio Apple` | Current price and percentage change. |
| `/comparar` | `/comparar BTC Oro` | Compares daily performance of two assets ("Oro" = gold). |
| `/explica` | `/explica Warrants` | AI definition of a financial term. |
| `/tendencia` | `/tendencia Tesla` | Bullish / bearish / sideways trend + AI comment. |
| `/como_invertir` | `/como_invertir` | Basic guide to the Bogleheads philosophy. |
| `/ayuda` | `/ayuda` | Quick list of commands. |

### Interactive menu

`/start` and inline buttons shortcut common actions (e.g. BTC price, IBEX trend, help). Callback routing is handled in `comandos/callbacks.py`.

---

## ⚠️ Disclaimer

Educational project only. Nothing the bot says is investment advice.

---

## 📁 Repository Structure

```
manuel_bot/
├── .env                          # Telegram token (not versioned)
├── .gitignore                    # Ignores .env
├── main.py                       # Entry point: Application + handler registration
├── config.py                     # TOKEN, Ollama URL/model, cache TTLs, MAPA_ACTIVOS
├── cerebro.py                    # Ollama + Yahoo, cache, aliases, confirmations, HTML output
├── requirements.txt              # Pinned Python dependencies
└── comandos/                     # One module per Telegram command
    ├── __init__.py               # Package marker
    ├── start.py                  # /start + main inline keyboard
    ├── precio.py                 # /precio
    ├── comparar.py               # /comparar
    ├── tendencia.py              # /tendencia
    ├── explica.py                # /explica
    ├── invertir.py               # /como_invertir
    ├── ayuda.py                  # /ayuda
    └── callbacks.py              # Inline-button handler (menu + ticker confirmations)
```

---

**Manuel Broker** · Real-time quotes, local AI and Telegram — without shipping your questions to the cloud.

Made with 🐍 Python, ❤️ and coffee.