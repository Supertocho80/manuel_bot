from telegram import Update
from telegram.ext import ContextTypes

async def como_invertir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    txt = (
        "🌱 <b>Guía Básica de Inversión (Filosofía Boglehead)</b>\n\n"
        "1. <b>Largo Plazo:</b> La inversión es una maratón, no un sprint. El interés compuesto necesita tiempo.\n"
        "2. <b>Diversificación:</b> <i>'No busques la aguja en el pajar, compra el pajar entero'</i>. Invierte en todo el mercado mundial.\n"
        "3. <b>Bajos Costes:</b> Las comisiones se comen tu rentabilidad. Los Fondos Indexados o ETFs son ideales.\n\n"
        "🧠 <b>¿Por dónde empiezo?</b>\n"
        "La estrategia más recomendada es la <b>inversión pasiva indexada</b>: simple, barata y estadísticamente superior a intentar adivinar qué acción subirá.\n\n"
        "📚 <b>La Biblia de la Inversión:</b>\n"
        "Para profundizar, consulta la guía oficial de la comunidad española:\n"
        "👉 <a href='https://bogleheads.es/guia/'>Guía Bogleheads España</a>"
    )
    # disable_web_page_preview=False permite que salga la previsualización del enlace
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt, parse_mode="HTML", disable_web_page_preview=False)
