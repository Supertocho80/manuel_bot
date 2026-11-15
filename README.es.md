# 🤖 Manuel Broker Bot

[English](README.md) | Español

**Manuel Broker** es un asistente financiero para Telegram desarrollado en Python. Combina datos de mercado en tiempo real (Yahoo Finance) con un **modelo de IA local** (Ollama + Phi-3 Mini) para dar cotizaciones, comparativas de activos, análisis de tendencia y explicaciones financieras sencillas, sin enviar nada a una IA en la nube.

## ✨ Características

* **💰 Precios en tiempo real:** acciones (Apple, Inditex…), índices (S&P 500, IBEX 35, Nasdaq), criptomonedas (Bitcoin, Ethereum…), materias primas (oro, plata) y EUR/USD.
* **🥊 Comparador de activos:** enfrenta dos activos según su rendimiento diario relativo.
* **🔮 Análisis de tendencia híbrido:** veredicto Alcista / Bajista / Lateral calculado con datos reales, más un breve comentario de la IA.
* **📖 Diccionario financiero con IA:** explica términos financieros de forma sencilla y rechaza temas no financieros.
* **🌱 Guía de inversión pasiva (Bogleheads):** nociones de diversificación e inversión a largo plazo.
* **🧠 Robustez:**
  * **Mapa de alias:** decenas de nombres cotidianos asociados a tickers (p. ej. "Manzana" → `AAPL`, "Zara" → `ITX.MC`, "Oro" → `GC=F`).
  * **Corrección de errores:** si no reconoce un ticker, la IA sugiere uno y el bot pide confirmación con botones.
  * **Caché en memoria:** datos de mercado durante 60 s y textos de la IA durante 300 s, para ahorrar llamadas a Yahoo y al modelo.
  * **Salida segura:** `html.escape` en todo lo que se envía al chat; respuestas encapsuladas entre `<<< >>>` y temperatura 0.0 para reducir alucinaciones.

## 🛠️ Stack tecnológico

| Área | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Framework del bot | `python-telegram-bot` 22 (asíncrono, `Application`, handlers de comandos y callbacks) |
| Datos de mercado | `yfinance` |
| IA local | API HTTP de Ollama (`http://localhost:11434/api/generate`), modelo `phi3:mini` |
| Configuración | `python-dotenv` (`.env`) |

## 🏗️ Estructura del proyecto

```
manuel_bot/
├── main.py            # Punto de entrada: crea la Application de Telegram y registra los handlers
├── config.py          # Token desde .env, URL y modelo de Ollama, TTL de caché, mapa alias → ticker
├── cerebro.py         # Lógica principal: llamadas a Ollama, datos de Yahoo, caché, adivinar tickers,
│                      # filtro de temas financieros, confirmaciones y formato de mensajes
├── comandos/          # Un módulo por comando
│   ├── start.py       # /start + menú interactivo
│   ├── precio.py      # /precio
│   ├── comparar.py    # /comparar
│   ├── tendencia.py   # /tendencia
│   ├── explica.py     # /explica
│   ├── invertir.py    # /como_invertir
│   ├── ayuda.py       # /ayuda
│   └── callbacks.py   # Handler de botones (menú y confirmaciones)
└── requirements.txt
```

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Supertocho80/manuel_bot.git
cd manuel_bot
```

### 2. Crear el entorno virtual e instalar dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### 3. Instalar Ollama y el modelo

```bash
ollama pull phi3:mini
ollama serve                    # si no está ya en marcha
```

### 4. Variables de entorno

Crea un archivo `.env` en la raíz del proyecto (no lo subas a Git):

```env
MANUELBROKER_TOKEN=TU_TOKEN_DE_BOTFATHER
```

### 5. Ejecutar el bot

```bash
python main.py
```

## 🎮 Comandos

| Comando | Ejemplo | Descripción |
| --- | --- | --- |
| `/start` | `/start` | Inicia el bot y muestra el menú interactivo. |
| `/precio` | `/precio Apple` | Precio actual y variación porcentual. |
| `/comparar` | `/comparar BTC Oro` | Compara el rendimiento diario de dos activos. |
| `/explica` | `/explica Warrants` | Definición de un término financiero generada por IA. |
| `/tendencia` | `/tendencia Tesla` | Tendencia alcista / bajista / lateral + comentario de la IA. |
| `/como_invertir` | `/como_invertir` | Guía básica de la filosofía Bogleheads. |
| `/ayuda` | `/ayuda` | Lista rápida de comandos. |

## ⚠️ Aviso

Proyecto educativo. Nada de lo que diga el bot es asesoramiento de inversión.

---

Hecho con 🐍 Python, ❤️ y café.
