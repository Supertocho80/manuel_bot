from telegram import Update, constants
from telegram.ext import ContextTypes
import html
from cerebro import limpiar_argumentos, es_termino_financiero, consultar_ia

async def explica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        args = limpiar_argumentos(context.args, modo="laxo")
        if not args:
            await context.bot.send_message(chat_id=chat_id, text="⚠️ Uso: `/explica [término]`")
            return
        termino = " ".join(args)
        
        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
        if not await es_termino_financiero(termino):
            await context.bot.send_message(chat_id=chat_id, text="⛔ Ese término no parece financiero.")
            return

        await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
        explicacion = await consultar_ia("Profesor Finanzas. Define breve. <<<EXPLICACIÓN>>>", f"Define: '{termino}'", usar_cache=True, clave_cache=f"EXPLICA_{termino.upper()}")
        
        await context.bot.send_message(chat_id=chat_id, text=f"📖 <b>{termino.title()} (Finanzas):</b>\n\n{html.escape(explicacion)}", parse_mode="HTML")
    except:
        await context.bot.send_message(chat_id=chat_id, text="❌ Error interno.")
