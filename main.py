from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import TOKEN
# Importamos los comandos de nuestra carpeta
from comandos.start import start
from comandos.precio import precio
from comandos.comparar import comparar
from comandos.tendencia import tendencia_logic
from comandos.explica import explica
from comandos.invertir import como_invertir
from comandos.ayuda import ayuda
from comandos.callbacks import button_handler

def main():
    print("🚀 Bot Iniciado (MODULAR)...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("precio", precio))
    app.add_handler(CommandHandler("comparar", comparar))
    app.add_handler(CommandHandler("tendencia", tendencia_logic))
    app.add_handler(CommandHandler("explica", explica))
    app.add_handler(CommandHandler("como_invertir", como_invertir))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CallbackQueryHandler(button_handler))

    app.run_polling()

if __name__ == "__main__":
    main()
