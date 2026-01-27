import os
from dotenv import load_dotenv

load_dotenv()

# --- CONSTANTES ---
TOKEN = os.getenv("MANUELBROKER_TOKEN")
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "phi3:mini"

# --- CACHÉ ---
CACHE_DATOS = {}
CACHE_TTL_DATOS = 60
CACHE_TTL_TEXTO = 300

# --- MAPA DE ACTIVOS ---
MAPA_ACTIVOS = {
    "BTC": "BTC-USD", "BITCOIN": "BTC-USD",
    "ETH": "ETH-USD", "ETHEREUM": "ETH-USD",
    "SOL": "SOL-USD", "SOLANA": "SOL-USD",
    "ADA": "ADA-USD", "CARDANO": "ADA-USD",
    "DOGE": "DOGE-USD",
    "IBEX": "^IBEX", "IBEX35": "^IBEX", "IBEX 35": "^IBEX",
    "SP500": "^GSPC", "S&P500": "^GSPC", "S&P": "^GSPC",
    "NASDAQ": "^IXIC", "NDX": "^NDX", "NASDAQ100": "^NDX",
    "DOW": "^DJI", "DOWJONES": "^DJI",
    "VIX": "^VIX",
    "ORO": "GC=F", "GOLD": "GC=F",
    "PLATA": "SI=F", "SILVER": "SI=F", "XAG": "SI=F",
    "EUR": "EURUSD=X", "DOLAR": "EURUSD=X", "USD": "EURUSD=X",
    "APPLE": "AAPL", "MANZANA": "AAPL", "AAPL": "AAPL",
    "MICROSOFT": "MSFT", "MSFT": "MSFT",
    "GOOGLE": "GOOGL", "ALPHABET": "GOOGL", "GOOG": "GOOGL",
    "AMAZON": "AMZN", "AMZN": "AMZN",
    "TESLA": "TSLA", "TSLA": "TSLA",
    "META": "META", "FACEBOOK": "META",
    "NETFLIX": "NFLX", "NVIDIA": "NVDA", "AMD": "AMD", "INTEL": "INTC",
    "INDITEX": "ITX.MC", "ZARA": "ITX.MC", "ITX": "ITX.MC",
    "BBVA": "BBVA.MC", "SANTANDER": "SAN.MC", "SAN": "SAN.MC",
    "TELEFONICA": "TEF.MC", "TEF": "TEF.MC", "IBERDROLA": "IBE.MC",
    "REPSOL": "REP.MC", "CAIXABANK": "CABK.MC", "AENA": "AENA.MC",
    "ENDESA": "ELE.MC", "NATURGY": "NTGY.MC", "IAG": "IAG.MC"
}
