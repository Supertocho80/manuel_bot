# 🤖 Manuel Broker Bot

**Manuel Broker** es un asistente financiero inteligente para Telegram desarrollado en Python. Combina la precisión de datos en tiempo real (Yahoo Finance) con la capacidad explicativa de una IA local (Ollama/Phi-3) para ofrecer análisis de mercado, educación financiera y comparativas de activos.

## ✨ Características Principales

* **💰 Precios en Tiempo Real:** Cotizaciones al instante de acciones (Apple, Inditex...), índices (S&P500, IBEX35), criptomonedas (Bitcoin) y materias primas.
* **🥊 Comparador de Activos:** Enfrenta dos activos para ver cuál tiene mejor rendimiento diario relativo.
* **🔮 Análisis de Tendencia Híbrido:**
  * **Lógica Matemática:** Calcula si la tendencia es Alcista, Bajista o Lateral basándose en datos reales.
  * **Comentario IA:** Genera un análisis técnico breve usando inteligencia artificial.
* **📖 Diccionario Financiero IA:** Explica conceptos complejos de forma sencilla. Incluye filtros inteligentes para rechazar temas no financieros.
* **🌱 Educación Financiera (Bogleheads):** Guía integrada sobre la filosofía de inversión pasiva, diversificación y largo plazo.
* **🧠 Inteligencia Robusta:**
  * **Mapa de Activos Ampliado:** Reconoce cientos de alias (ej: "Manzana" -> AAPL, "Zara" -> ITX.MC).
  * **Corrección de Typos:** Si escribes mal un ticker, la IA intenta adivinarlo.
  * **Sanitización HTML:** Blindaje contra errores de formato y caracteres especiales.
  * **Anti-Alucinaciones:** Encapsulamiento de respuestas (`<<< >>>`) y temperatura 0.0 para máxima precisión.

## 🛠️ Requisitos Técnicos

1. **Python 3.10+**
2. **Ollama** instalado y ejecutándose localmente.
3. **Modelo de IA:** `phi3:mini` (Optimizado para velocidad y bajo consumo).

## 🚀 Instalación y Puesta en Marcha

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/manuel_bot.git](https://github.com/tu-usuario/manuel_bot.git)
cd manuel_bot

```

### 2. Configurar el entorno virtual

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

```

### 3. Instalar dependencias

```bash
pip install python-telegram-bot yfinance requests python-dotenv

```

### 4. Configurar Ollama

Asegúrate de tener Ollama corriendo y descarga el modelo:

```bash
ollama pull phi3:mini

```

### 5. Configurar Variables de Entorno

Crea un archivo llamado `.env` en la raíz del proyecto y añade tu token de Telegram:

```env
MANUELBROKER_TOKEN=TU_TOKEN_AQUI_OBTENIDO_DE_BOTFATHER

```

### 6. Ejecutar el Bot

```bash
python main.py

```

## 🎮 Comandos Disponibles

| Comando | Ejemplo | Descripción |
| --- | --- | --- |
| `/start` | `/start` | Inicia el bot y muestra el menú interactivo. |
| `/precio` | `/precio Apple` | Muestra precio actual y variación porcentual. |
| `/comparar` | `/comparar BTC Oro` | Compara el rendimiento diario de dos activos. |
| `/explica` | `/explica Warrants` | Definición generada por IA (filtro financiero activo). |
| `/tendencia` | `/tendencia Tesla` | Análisis de sentimiento (Alcista/Bajista) + Comentario. |
| `/como_invertir` | `/como_invertir` | Guía básica sobre la filosofía Bogleheads. |
| `/ayuda` | `/ayuda` | Lista rápida de comandos. |

## 🏗️ Arquitectura del Código

* **`main.py`:** Núcleo asíncrono. Gestiona los updates de Telegram, el caché en memoria y la lógica de negocio.
* **Integración IA:** Comunicación vía HTTP con Ollama, usando prompts de sistema estrictos y limpieza de respuestas con Regex.
* **Datos de Mercado:** Uso de `yfinance` para obtener datos OHLC (Open, High, Low, Close) y calcular variaciones.
* **Seguridad:** Uso de `html.escape` para prevenir inyecciones de código en el chat y `try-except` globales para evitar caídas del bot.

---

Hecho con 🐍 Python, ❤️ y Café.
