# 🤖 Manuel Broker Bot

[English](README.md) | Español

![Python](https://img.shields.io/badge/Python-3.10+-3776AB.svg?logo=python&logoColor=white)
![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-22-229ED9.svg?logo=telegram&logoColor=white)
![yfinance](https://img.shields.io/badge/yfinance-market%20data-00A86B.svg)
![Ollama](https://img.shields.io/badge/Ollama-local%20AI-000000.svg)
![Phi--3](https://img.shields.io/badge/Model-phi3%3Amini-8B5CF6.svg)
![dotenv](https://img.shields.io/badge/dotenv-config-ECD53F.svg)

> **Estado: proyecto educativo.** Asistente financiero en Telegram que mantiene datos de mercado e inferencia de IA en tu máquina — Yahoo Finance para cotizaciones, Ollama para explicaciones.

**Manuel Broker** es un bot en Python para Telegram. Combina datos de mercado en tiempo real con un **modelo de IA local** (Ollama + Phi-3 Mini) para ofrecer cotizaciones, comparativas, análisis de tendencia y definiciones financieras sencillas sin enviar los mensajes del usuario a un LLM en la nube.

---

## 🚀 Arquitectura y Stack Tecnológico

El código es **modular**: `main.py` monta la `Application` de Telegram, cada comando vive en `comandos/` y la lógica compartida (Yahoo, Ollama, caché, alias, confirmaciones) está en `cerebro.py`.

| Capa | Tecnología |
|------|------------|
| **Runtime** | Python 3.10+ |
| **Framework del bot** | `python-telegram-bot` 22 — `Application` asíncrona, handlers de comandos y callbacks |
| **Datos de mercado** | `yfinance` (OHLC, variación diaria) |
| **IA local** | API HTTP de Ollama (`http://localhost:11434/api/generate`), modelo `phi3:mini` |
| **Configuración** | `python-dotenv` — `MANUELBROKER_TOKEN` en `.env` |
| **Caché** | Diccionario en memoria en `cerebro.py` — datos de mercado 60 s, texto IA 300 s |

```
┌──────────────┐   API de Telegram   ┌─────────────────────────────────────┐
│  Chat usuario│ ◄──────────────────► │  main.py + comandos/ (handlers)     │
└──────────────┘                    └──────────────────┬──────────────────┘
                                                     │
                         ┌───────────────────────────▼───────────────────────────┐
                         │  cerebro.py — alias, caché, confirmaciones, formato HTML │
                         └─────────────┬───────────────────────┬─────────────┘
                                       │                       │
                            ┌──────────▼──────────┐   ┌──────────▼──────────┐
                            │  Yahoo (yfinance)   │   │  Ollama (phi3:mini) │
                            └─────────────────────┘   └─────────────────────┘
```

---

## ✨ Características Principales

| Característica | Qué hace |
|----------------|----------|
| **Precios en tiempo real** | Acciones, índices, cripto, materias primas y EUR/USD vía mapa de alias (p. ej. "Manzana" → `AAPL`, "Oro" → `GC=F`). |
| **Comparador de activos** | Rendimiento diario relativo entre dos tickers o alias. |
| **Tendencia híbrida** | Veredicto Alcista / Bajista / Lateral con matemáticas sobre el precio, más un breve comentario de la IA. |
| **Diccionario financiero** | `/explica` define términos con IA; se rechazan temas no financieros. |
| **Guía de inversión pasiva** | `/como_invertir` — nociones estilo Bogleheads. |
| **Recuperación de typos** | Tickers desconocidos activan sugerencia de la IA y botones de confirmación. |
| **Salida segura en el chat** | `html.escape` en mensajes; respuestas IA con envoltorio `<<< >>>` y temperatura `0.0`. |

---

## ⚙️ Requisitos Previos

| Herramienta | Notas |
|-------------|--------|
| **Python** | 3.10 o superior |
| **Ollama** | En ejecución local; modelo `phi3:mini` descargado |
| **Token de bot de Telegram** | Desde [@BotFather](https://t.me/BotFather) |
| **Internet** | Para Telegram y Yahoo Finance (no para IA en la nube) |

---

## 📦 Instalación y Arranque

### Paso 0 · Variables de entorno (obligatorio)

Crea **`.env` en la raíz del repositorio** (listado en `.gitignore`):

```env
MANUELBROKER_TOKEN=TU_TOKEN_DE_BOTFATHER
```

### Paso 1 · Clonar el repositorio

```bash
git clone https://github.com/Supertocho80/manuel_bot.git
cd manuel_bot
```

### Paso 2 · Entorno virtual y dependencias

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
```

### Paso 3 · Ollama y el modelo

```bash
ollama pull phi3:mini
ollama serve                    # si no está ya en marcha
```

### Paso 4 · Ejecutar el bot

```bash
python main.py
```

---

## 📖 Guía de Uso

El bot conversa en **español**; los nombres de los comandos son en español.

### Comandos

| Comando | Ejemplo | Descripción |
| --- | --- | --- |
| `/start` | `/start` | Inicia el bot y muestra el menú interactivo. |
| `/precio` | `/precio Apple` | Precio actual y variación porcentual. |
| `/comparar` | `/comparar BTC Oro` | Compara el rendimiento diario de dos activos. |
| `/explica` | `/explica Warrants` | Definición de un término financiero generada por IA. |
| `/tendencia` | `/tendencia Tesla` | Tendencia alcista / bajista / lateral + comentario de la IA. |
| `/como_invertir` | `/como_invertir` | Guía básica de la filosofía Bogleheads. |
| `/ayuda` | `/ayuda` | Lista rápida de comandos. |

### Menú interactivo

`/start` y los botones en línea acortan acciones habituales (p. ej. precio de BTC, tendencia del IBEX, ayuda). El enrutado de callbacks está en `comandos/callbacks.py`.

---

## ⚠️ Aviso

Proyecto solo educativo. Nada de lo que diga el bot es asesoramiento de inversión.

---

## 📁 Estructura del Repositorio

```
manuel_bot/
├── .env                          # Token de Telegram (no versionado)
├── .gitignore                    # Ignora .env
├── main.py                       # Punto de entrada: Application + registro de handlers
├── config.py                     # TOKEN, URL/modelo Ollama, TTL de caché, MAPA_ACTIVOS
├── cerebro.py                    # Ollama + Yahoo, caché, alias, confirmaciones, salida HTML
├── requirements.txt              # Dependencias Python fijadas
└── comandos/                     # Un módulo por comando de Telegram
    ├── __init__.py               # Marcador del paquete
    ├── start.py                  # /start + teclado inline principal
    ├── precio.py                 # /precio
    ├── comparar.py               # /comparar
    ├── tendencia.py              # /tendencia
    ├── explica.py                # /explica
    ├── invertir.py               # /como_invertir
    ├── ayuda.py                  # /ayuda
    └── callbacks.py              # Handler de botones (menú + confirmación de tickers)
```

---

**Manuel Broker** · Cotizaciones en tiempo real, IA local y Telegram — sin mandar tus preguntas a la nube.

Hecho con 🐍 Python, ❤️ y café.