import time
import asyncio
import requests
import re
import html
import yfinance as yf
from functools import partial
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, constants
from config import * # Importamos TOKEN, MODELO, URLs y MAPA_ACTIVOS

# ==============================================================================
# 🧠 INTELIGENCIA ARTIFICIAL (OLLAMA)
# ==============================================================================

def _consultar_ia_sync(sistema, usuario):
    try:
        prompt_final = (
            f"{sistema}\n"
            f"USUARIO: {usuario}\n"
            "INSTRUCCIÓN: Responde DENTRO de <<< >>>.\n"
            "RESPUESTA:"
        )
        payload = {
            "model": MODELO,
            "prompt": prompt_final,
            "stream": False,
            "options": {
                "temperature": 0.0,
                "stop": [">>>", "User:", "SISTEMA:", "INSTRUCCIÓN:"]
            }
        }
        r = requests.post(OLLAMA_URL, json=payload, timeout=120)

        if r.status_code == 200:
            texto = r.json().get("response", "").strip()

            # Limpieza de basura
            basura = ["end of one possible answer", "|>", "SISTEMA:", "INSTRUCCIÓN:", "User:", "Assistant:"]
            for b in basura:
                texto = texto.replace(b, "")

            # Extracción <<< >>>
            match = re.search(r"<<<(.*?)>>>", texto + ">>>", re.DOTALL)
            resultado = texto 
            if match:
                contenido = match.group(1).strip()
                if contenido: resultado = contenido
            elif "\n" in texto:
                resultado = texto.split("\n")[-1]

            return resultado.replace("<<<", "").replace(">>>", "").replace('"', "").strip()

        return "⚠️ Error IA."
    except Exception as e:
        print(f"❌ Error IA: {e}")
        return "⚠️ IA dormida."

async def consultar_ia(sistema, usuario, usar_cache=False, clave_cache=None):
    if usar_cache and clave_cache:
        ahora = time.time()
        # CACHE_DATOS viene de config.py, pero al importarlo * se crea una copia local en el namespace.
        # Para que el caché funcione bien entre módulos, idealmente debería ser un objeto compartido,
        # pero para este script simple funcionará si importamos el diccionario.
        # NOTA: En estructuras complejas, mejor usar un Singleton o Redis.
        if clave_cache in CACHE_DATOS:
            res, timestamp = CACHE_DATOS[clave_cache]
            if ahora - timestamp < CACHE_TTL_TEXTO:
                print(f"⚡ [CACHE] Texto recuperado: {clave_cache}")
                return res

    print(f"🤖 [IA] Prompt: {usuario}")
    loop = asyncio.get_running_loop()
    respuesta = await loop.run_in_executor(None, partial(_consultar_ia_sync, sistema, usuario))

    if usar_cache and clave_cache and respuesta and "⚠️" not in respuesta:
        CACHE_DATOS[clave_cache] = (respuesta, time.time())

    return respuesta

# ==============================================================================
# 📡 DATOS DE MERCADO (YAHOO FINANCE)
# ==============================================================================

def _obtener_datos_sync(ticker):
    try:
        t = yf.Ticker(ticker)
        h = t.history(period="1d")
        if h.empty: return None

        precio = h["Close"].iloc[-1]
        es_euro = any(x in ticker for x in [".MC", ".DE", ".PA", "^IBEX", "EUR=X"])
        moneda = "€" if es_euro else "$"

        return {
            "symbol": ticker,
            "precio": precio,
            "moneda": moneda,
            "cambio": ((h["Close"].iloc[-1] - h["Open"].iloc[-1]) / h["Open"].iloc[-1]) * 100,
        }
    except:
        return None

async def obtener_datos(ticker):
    ahora = time.time()
    if ticker in CACHE_DATOS:
        datos, timestamp = CACHE_DATOS[ticker]
        if ahora - timestamp < CACHE_TTL_DATOS:
            print(f"⚡ [CACHE] Sirviendo datos {ticker}")
            return datos

    print(f"📡 [YAHOO] Descargando {ticker}...")
    loop = asyncio.get_running_loop()
    datos = await loop.run_in_executor(None, _obtener_datos_sync, ticker)

    if datos:
        CACHE_DATOS[ticker] = (datos, ahora)
    return datos

# ==============================================================================
# 🛠️ UTILIDADES (Filtros, Limpieza, IA Auxiliar)
# ==============================================================================

def limpiar_argumentos(lista_args, modo="estricto"):
    if modo == "estricto":
        prohibidas = ["EN", "EUROS", "EURO", "DOLAR", "DOLARES", "EL", "LA", "DE", "VS", "CONTRA", "QUE", "ES", "SON", "Y"]
        return [arg for arg in lista_args if arg.upper() not in prohibidas]
    else:
        prohibidas = ["/EXPLICA", "POR", "FAVOR", "EXPLICA", "QUE", "ES"]
        return [arg for arg in lista_args if arg.upper() not in prohibidas]

async def adivinar_ticker_ia(busqueda):
    sistema = "Experto Yahoo Finance. Corrige typos.\nApple -> AAPL\nInditex -> ITX.MC\nResponde SOLO: <<<TICKER>>>."
    res = await consultar_ia(sistema, f"Ticker de: {busqueda}")
    match = re.search(r"\b[A-Z0-9^.-]{2,10}\b", res.upper())
    return match.group(0) if match else None

# --- ESTA ES LA FUNCIÓN QUE FALTABA ---
async def es_termino_financiero(termino):
    try:
        term_upper = termino.upper()
        whitelist = [
            "FOREX", "BITCOIN", "BTC", "ETHEREUM", "ETH", "CRYPTO", "CRIPTO",
            "TRADING", "INVERSION", "BOLSA", "NASDAQ", "SP500", "IBEX",
            "DINERO", "DOLAR", "EURO", "ORO", "ETF", "FUTURO", "OPCION",
            "DIVISA", "BANCO", "INTERES", "DEUDA", "AHORRO", "ACCION",
            "CALL", "PUT", "WARRANT", "BONO", "LETRA"
        ]

        if any(w in term_upper for w in whitelist):
            print(f"✅ [FILTRO] '{termino}' aceptado por Lista Blanca.")
            return True

        sistema = (
            "CLASIFICADOR DE TEMÁTICA.\n"
            "Analiza si el término pertenece a: Finanzas, Bolsa, Criptos, Banca, Negocios.\n"
            "SI pertenece -> Responde <<<SI>>>\n"
            "SI es cocina, deportes, etc -> Responde <<<NO>>>"
        )
        res = await consultar_ia(sistema, f"Clasifica: '{termino}'")

        if not res or "⚠️" in res: return False
        es_financiero = "SI" in str(res).upper()
        print(f"🤖 [FILTRO IA] '{termino}' -> {res} -> {'Aceptado' if es_financiero else 'Rechazado'}")
        return es_financiero

    except Exception as e:
        print(f"❌ Error CRÍTICO en filtro: {e}")
        return False

# ==============================================================================
# 🎮 LÓGICA DE CONTROL Y RESPUESTAS VISUALES
# ==============================================================================

async def pedir_confirmacion(update, context, accion, input_user, sugerencia, extra_info="0"):
    texto = f"🤔 No encontré <b>{html.escape(input_user)}</b>.\n¿Te refieres a <b>{html.escape(sugerencia)}</b>?"
    payload_si = f"conf|{accion}|{sugerencia}|{extra_info}"
    payload_no = "conf|cancel|0|0"

    keyboard = [[
        InlineKeyboardButton("✅ Sí", callback_data=payload_si),
        InlineKeyboardButton("❌ No", callback_data=payload_no),
    ]]
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=texto,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="HTML",
    )

async def mostrar_precio(chat_id, context, datos):
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
    prompt = (
        f"El activo {datos['symbol']} vale {datos['precio']:.2f}. Varió {datos['cambio']:.2f}%.\n"
        "Dame un comentario técnico de 1 frase.\n"
        "Encierra la respuesta en: <<< TU FRASE >>>"
    )
    ia_msg = await consultar_ia("Analista Breve", prompt)

    txt = (
        f"💰 <b>{datos['symbol']}</b>\n"
        f"💵 Precio: <b>{datos['precio']:,.2f} {datos['moneda']}</b>\n"
        f"📈 Var: <b>{datos['cambio']:+.2f}%</b>\n\n"
        f"🤖 {html.escape(ia_msg)}"
    )
    await context.bot.send_message(chat_id=chat_id, text=txt, parse_mode="HTML")

async def mostrar_comparativa(chat_id, context, d1, d2):
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
    prompt = (
        f"Compara {d1['symbol']} ({d1['cambio']:.2f}%) vs {d2['symbol']} ({d2['cambio']:.2f}%).\n"
        "¿Quién gana hoy? Max 15 palabras.\n"
        "Encierra la respuesta en: <<< TU RESPUESTA >>>"
    )
    conclusion = await consultar_ia("Juez Financiero", prompt)

    txt = (
        f"🥊 <b>VS</b>\n"
        f"🔹 {d1['symbol']}: {d1['precio']:,.2f} {d1['moneda']} <b>({d1['cambio']:+.2f}%)</b>\n"
        f"🔸 {d2['symbol']}: {d2['precio']:,.2f} {d2['moneda']} <b>({d2['cambio']:+.2f}%)</b>\n\n"
        f"🏆 {html.escape(conclusion)}"
    )
    await context.bot.send_message(chat_id=chat_id, text=txt, parse_mode="HTML")

async def mostrar_tendencia(chat_id, context, datos):
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
    
    cambio = datos['cambio']
    if cambio > 0.05:
        sentimiento = "ALCISTA 🟢"
        instruccion = "tendencia alcista"
    elif cambio < -0.05:
        sentimiento = "BAJISTA 🔴"
        instruccion = "tendencia bajista"
    else:
        sentimiento = "NEUTRO/LATERAL 🟡"
        instruccion = "mercado lateral o indeciso"

    prompt = (
        f"Activo: {datos['symbol']}.\n"
        f"Variación: {datos['cambio']:.2f}% ({instruccion}).\n"
        "Escribe una frase corta de analista confirmando el movimiento.\n"
        "Encierra la respuesta en: <<< TU FRASE >>>"
    )
    analisis = await consultar_ia("Analista de Tendencias", prompt)

    txt = (
        f"🔮 <b>Tendencia: {datos['symbol']}</b>\n"
        f"📊 Var Hoy: <b>{datos['cambio']:+.2f}%</b>\n"
        f"🧭 Señal: <b>{sentimiento}</b>\n\n"
        f"📉 {html.escape(analisis)}"
    )
    await context.bot.send_message(chat_id=chat_id, text=txt, parse_mode="HTML")

async def verificar_y_ejecutar(update, context, accion, activo1, activo2=None):
    chat_id = update.effective_chat.id
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)

    # 1. Búsqueda Directa
    t1_candidato = MAPA_ACTIVOS.get(activo1.upper(), activo1.upper())
    d1 = await obtener_datos(t1_candidato)

    # 2. IA / Sugerencias
    if not d1:
        sugerencia = await adivinar_ticker_ia(activo1)
        if sugerencia and sugerencia != t1_candidato:
            extra = activo2 if accion == "cmp" else "0"
            await pedir_confirmacion(update, context, accion, activo1, sugerencia, extra_info=extra)
            return
        else:
            await context.bot.send_message(chat_id, "❌ Lo siento, no encontré ese activo. Prueba con el Ticker exacto.")
            return

    # 3. Validar Activo 2 (Solo Comparar)
    d2 = None
    if accion == "cmp" and activo2:
        t2_candidato = MAPA_ACTIVOS.get(activo2.upper(), activo2.upper())
        d2 = await obtener_datos(t2_candidato)

        if not d2:
            sugerencia = await adivinar_ticker_ia(activo2)
            if sugerencia and sugerencia != t2_candidato:
                await pedir_confirmacion(update, context, "cmp_2", activo2, sugerencia, extra_info=d1["symbol"])
                return
            else:
                await context.bot.send_message(chat_id, "❌ Lo siento, no encontré el segundo activo.")
                return

    # 4. Ejecución final
    if accion == "prc":
        await mostrar_precio(chat_id, context, d1)
    elif accion == "cmp":
        await mostrar_comparativa(chat_id, context, d1, d2)
    elif accion == "tnd":
        await mostrar_tendencia(chat_id, context, d1)
