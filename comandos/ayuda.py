from telegram import Update
from telegram.ext import ContextTypes

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "🤖 <b>COMANDOS MANUEL BROKER</b>\n\n"
        "• <code>/start</code> - Inicio\n"
        "• <code>/precio</code> [activo]\n"
        "• <code>/comparar</code> [A] [B]\n"
        "• <code>/explica</code> [termino]\n"
        "• <code>/tendencia</code> [activo]\n"
        "• <code>/como_invertir</code> - Guía"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt, parse_mode="HTML")
