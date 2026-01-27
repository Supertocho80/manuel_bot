from telegram import Update
from telegram.ext import ContextTypes
from cerebro import limpiar_argumentos, verificar_y_ejecutar

async def precio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = limpiar_argumentos(context.args, modo="estricto")
    if not args:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Escribe: `/precio [activo]`")
        return
    await verificar_y_ejecutar(update, context, "prc", " ".join(args))
