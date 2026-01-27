from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = "¡Bienvenido a Manuel Broker! 👋\n\nToda la info financiera, sin complicaciones.\n\n✨ <b>Menú Principal:</b>"
    kb = [
        [InlineKeyboardButton("💰 Bitcoin", callback_data="precio_BTC"), InlineKeyboardButton("🇪🇸 Ibex 35", callback_data="precio_IBEX")],
        [InlineKeyboardButton("🔮 S&P500", callback_data="tendencia"), InlineKeyboardButton("📖 Aprender", callback_data="explica_btn")],
        [InlineKeyboardButton("🌱 Invertir", callback_data="invertir_btn"), InlineKeyboardButton("❓ Ayuda", callback_data="ayuda")],
    ]
    if update.callback_query:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=texto, reply_markup=InlineKeyboardMarkup(kb), parse_mode="HTML")
    else:
        await update.message.reply_html(texto, reply_markup=InlineKeyboardMarkup(kb))
