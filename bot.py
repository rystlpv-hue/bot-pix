import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
PIX_CHAVE = os.getenv("PIX_CHAVE")

bot = telebot.TeleBot(TOKEN)

PRECOS = {
    "plano1": {"nome": "Plano Básico", "valor": "19,90"},
    "plano2": {"nome": "Plano Médio", "valor": "29,90"},
    "plano3": {"nome": "Plano Premium", "valor": "49,90"},
}

@bot.message_handler(commands=['start', 'menu'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    for key, info in PRECOS.items():
        btn = types.InlineKeyboardButton(
            text=f"{info['nome']} - R$ {info['valor']}",
            callback_data=key
        )
        markup.add(btn)
    
    bot.send_message(
        message.chat.id,
        "Escolha o plano que deseja:\n\nApós escolher, você receberá a chave PIX.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data in PRECOS:
        plano = PRECOS[call.data]
        
        texto = f"""
✅ *Pagamento gerado*

Plano: *{plano['nome']}*
Valor: *R$ {plano['valor']}*

🔑 *Chave PIX:*
`{PIX_CHAVE}`

➡️ Copie a chave acima e faça o pagamento no valor exato.

Após o pagamento, envie o comprovante aqui.
"""
        bot.send_message(call.message.chat.id, texto, parse_mode="Markdown")
        bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: True)
def qualquer_mensagem(message):
    bot.reply_to(message, "Use /start para ver os planos disponíveis.")

print("Bot iniciado...")
bot.infinity_polling()