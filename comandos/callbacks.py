from telegram import Update
from telegram.ext import ContextTypes
from cerebro import obtener_datos, mostrar_precio, mostrar_tendencia, mostrar_comparativa, verificar_y_ejecutar
from comandos.invertir import como_invertir
from comandos.ayuda import ayuda

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    chat_id = query.message.chat_id

    if data.startswith("conf|"):
        _, accion, sugerencia, extra = data.split("|")
        await query.delete_message()
        if accion == "cancel":
            await context.bot.send_message(chat_id, "❌ Cancelado.")
        elif accion == "prc":
            d = await obtener_datos(sugerencia)
            if d: await mostrar_precio(chat_id, context, d)
        elif accion == "tnd":
            d = await obtener_datos(sugerencia)
            if d: await mostrar_tendencia(chat_id, context, d)
        elif accion == "cmp":
            await verificar_y_ejecutar(update, context, "cmp", sugerencia, extra)
        elif accion == "cmp_2":
            d1 = await obtener_datos(extra)
            d2 = await obtener_datos(sugerencia)
            if d1 and d2: await mostrar_comparativa(chat_id, context, d1, d2)
        return

    if data.startswith("precio_"): await verificar_y_ejecutar(update, context, "prc", data.split("_")[1])
    elif data == "tendencia": await verificar_y_ejecutar(update, context, "tnd", "^GSPC")
    elif data == "invertir_btn": await como_invertir(update, context)
    elif data == "ayuda": await ayuda(update, context)
    elif data == "explica_btn": await context.bot.send_message(chat_id, "ℹ️ Ej: `/explica Pignoracion`")
