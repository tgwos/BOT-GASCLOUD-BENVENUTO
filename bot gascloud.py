from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)
from flask import Flask
from threading import Thread
import os

TOKEN = os.environ['TOKEN']  # prende il token dai Secrets di Replit
CANAL_TELEGRAM = "t.me/+iMgIPdF4HPswMDRh"  # link del canale

# ===== WEB SERVER PER REPLIT 24/7 =====
app_web = Flask('')

@app_web.route('/')
def home():
    return "Bot Gas Cloud attivo!"

def run_web():
    app_web.run(host='0.0.0.0', port=8080)

Thread(target=run_web).start()

# ===== MENU PRINCIPALE =====
def menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛒 Catalogo", callback_data="catalogo")],
        [InlineKeyboardButton("💳 Metodi di pagamento", callback_data="pagamenti")],
        [InlineKeyboardButton("📦 Info spedizione", callback_data="spedizione")],
        [InlineKeyboardButton("📩 Contattami", url="https://t.me/gascloud2")]
    ])

# ===== START E TORNA AL MENU =====
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

# ===== CONTROLLO ISCRIZIONE =====
async def check_membership(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CANAL_TELEGRAM, user_id=user_id)
        if member.status in ["member", "creator", "administrator"]:
            return True
        return False
    except:
        return False

# ===== CATALOGO =====
async def catalogo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = update.callback_query.from_user.id
    is_member = await check_membership(user_id, context)

    if is_member:
        await update.callback_query.message.edit_text(
            "🛒 *Apri il catalogo qui:*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Apri Catalogo", url="https://tgwos.github.io/mini-app/index.html")],
                [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await update.callback_query.message.edit_text(
            "🔒 Devi iscriverti al canale per accedere al catalogo:\n"
            f"{CANAL_TELEGRAM}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Controlla iscrizione", callback_data="check_subscription")],
                [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
            ])
        )

# ===== CONTROLLA ISCRIZIONE (DOPO CHE SI SONO ISCRITTI) =====
async def check_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = update.callback_query.from_user.id
    is_member = await check_membership(user_id, context)

    if is_member:
        await update.callback_query.message.edit_text(
            "🛒 *Apri il catalogo qui:*",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🛒 Apri Catalogo", url="https://tgwos.github.io/mini-app/index.html")],
                [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
            ]),
            parse_mode="Markdown"
        )
    else:
        await update.callback_query.message.edit_text(
            "🔒 Devi ancora iscriverti al canale per accedere al catalogo:\n"
            f"{CANAL_TELEGRAM}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Controlla iscrizione", callback_data="check_subscription")],
                [InlineKeyboardButton("🔙 Torna al menu", callback_data="menu")]
            ])
        )

# ===== METODI DI PAGAMENTO =====
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

# ===== INFO SPEDIZIONE =====
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
        "https://inpost.it/trova-un-locker",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# ===== AVVIO BOT =====
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(catalogo, pattern="catalogo"))
app.add_handler(CallbackQueryHandler(check_subscription, pattern="check_subscription"))
app.add_handler(CallbackQueryHandler(pagamenti, pattern="pagamenti"))
app.add_handler(CallbackQueryHandler(spedizione, pattern="spedizione"))
app.add_handler(CallbackQueryHandler(start, pattern="menu"))

print("🤖 Bot avviato...")
app.run_polling()

