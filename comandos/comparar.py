from telegram import Update
from telegram.ext import ContextTypes
from cerebro import limpiar_argumentos, verificar_y_ejecutar

async def comparar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = limpiar_argumentos(context.args, modo="estricto")
    if len(args) < 2:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="⚠️ Uso: `/comparar [A] [B]`")
        return
    await verificar_y_ejecutar(update, context, "cmp", args[0], args[1])
