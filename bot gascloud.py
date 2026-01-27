from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

import os
TOKEN = os.environ['TOKEN']

CANAL_TELEGRAM = "t.me/+iMgIPdF4HPswMDRh"  # Inserisci l'username del canale o il link corto senza https://t.me/

# 🔹 MENU PRINCIPALE
def menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Catalogo", callback_data="catalogo")],
        [InlineKeyboardButton("💳 Metodi di pagamento", callback_data="pagamenti")],
        [InlineKeyboardButton("📦 Info spedizione", callback_data="spedizione")],
        [InlineKeyboardButton("📩 Contattami", url="https://t.me/gascloud2")]
    ])

# 🔹 /start e TORNA AL MENU
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🏠 *Menu principale Gas Cloud* ☁️🔥\n\n"
        "Scegli un'opzione dal menu qui sotto 👇"
    )

    if update.message:
        await update.message.reply_text(
            text,
            reply_markup=menu_keyboard(),
            parse_mode="Markdown"
        )
    else:
        await update.callback_query.answer()
        await update.callback_query.message.edit_text(
            text,
            reply_markup=menu_keyboard(),
            parse_mode="Markdown"
        )

# 🔹 CONTROLLO ISCRIZIONE AL CANALE
async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CANAL_TELEGRAM, user_id=user_id)
        if member.status in ["member", "creator", "administrator"]:
            return True
        else:
            return False
    except:
        return False

# 🔹 CATALOGO (blocca ai non iscritti)
async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    is_member = await check_membership(update, context)
    
    if is_member:
        # Se è iscritto, apri mini app con link
        await update.callback_query.message.edit_text(
            "🛒 *Apri il catalogo qui:*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Apri Catalogo", url="https://tgwos.github.io/mini-app/index.html")],
                [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )
    else:
        # Se non è iscritto
        await update.callback_query.message.edit_text(
            "🔒 Devi iscriverti al canale per accedere al catalogo:\n"
            f"{CANAL_TELEGRAM}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
            ])
        )

# 🔹 METODI DI PAGAMENTO
async def pagamenti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
    ])

    await update.callback_query.message.edit_text(
        "💳 *Metodi di pagamento disponibili:*\n\n"
        "✅ +7% Postepay\n"
        "✅ +7% Bonifico bancario\n"
        "✅ +0% Crypto\n\n"
        "📌 Per procedere con il pagamento contattaci in privato.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# 🔹 INFO SPEDIZIONE
async def spedizione(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
    ])

    await update.callback_query.message.edit_text(
        "📦 *Info spedizione*\n\n"
        "Abbiamo la possibilità di spedire con vari corrieri, ma preferiamo sempre "
        "utilizzare *InPost* perché ci dà la possibilità di spedire in totale anonimato.\n\n"
        "❌ Non serve nome e cognome\n"
        "✅ Serve solo una *email*\n\n"
        "📩 Riceverai un *QR code* con cui potrai ritirare il tuo pacco "
        "in qualsiasi punto InPost.\n\n"
        "📍 Trova il locker più vicino a te qui:\n"

