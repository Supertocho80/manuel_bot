# 🤖 Manuel Broker Bot

**Manuel Broker** es un asistente financiero inteligente para Telegram. Combina la precisión de datos en tiempo real (Yahoo Finance) con la capacidad explicativa de una IA local (Ollama/Phi-3).

## ✨ Características

* **💰 Precios en Tiempo Real:** Consulta acciones, criptos, divisas y materias primas.
    * *Comando:* `/precio [activo]`
* **🥊 Comparador de Activos:** Enfrenta dos activos para ver cuál rinde mejor hoy.
    * *Comando:* `/comparar [A] [B]`
* **🔮 Análisis de Tendencia:** Detecta matemáticamente si el mercado es Alcista o Bajista y genera un análisis con IA.
    * *Comando:* `/tendencia [activo]` (Por defecto: S&P 500)
* **📖 Diccionario Financiero:** Explica conceptos complejos. Incluye filtros para evitar preguntas no financieras.
    * *Comando:* `/explica [término]`
* **🧠 IA Híbrida & Asíncrona:**
    * No se bloquea mientras "piensa".
    * Corrige errores tipográficos automáticamente (ej: "bicoin" -> BTC).
    * Sistema de caché para respuestas ultrarrápidas.

## 🛠️ Requisitos

1.  **Python 3.10+**
2.  **Ollama** instalado y ejecutándose localmente.
    * Modelo: `ollama pull phi3:mini`

## 🚀 Instalación

1.  **Clonar y preparar entorno:**
    ```bash
    git clone [https://github.com/tu-usuario/manuel_bot.git](https://github.com/tu-usuario/manuel_bot.git)
    cd manuel_bot
    python -m venv venv
    source venv/bin/activate  # O venv\Scripts\activate en Windows
    ```

2.  **Instalar dependencias:**
    ```bash
    pip install python-telegram-bot yfinance requests python-dotenv
    ```

3.  **Configuración:**
    Crea un archivo `.env` en la raíz con tu token:
    ```env
    MANUELBROKER_TOKEN=TU_TOKEN_DE_TELEGRAM
    ```

4.  **Ejecutar:**
    ```bash
    python main.py
    ```

## 🐛 Solución de Problemas Comunes

* **"Error IA":** Asegúrate de que Ollama está corriendo (`ollama serve`).
* **El bot no responde:** Revisa que el token en `.env` sea correcto.
* **Respuestas cortadas:** El bot usa sanitización HTML para evitar conflictos con caracteres especiales.

---
Hecho con 🐍 Python y mucha cafeína.
