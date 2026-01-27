from telegram import Update
from telegram.ext import ContextTypes
from cerebro import limpiar_argumentos, verificar_y_ejecutar

async def tendencia_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = []
    if context.args: args = limpiar_argumentos(context.args, modo="estricto")
    activo = " ".join(args) if args else "^GSPC"
    await verificar_y_ejecutar(update, context, "tnd", activo)
