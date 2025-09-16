from openai import OpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


# Inicializa o cliente
client = OpenAI(api_key="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")
TOKEN = '8351664504:AAHdmIRtCOWTk4rkQJpzZRg8LQkSE1cGPyQ'
#USER: @eng8_2025_2_bot

# Mantém o histórico da conversa
messages = [
    {"role": "system", "content": "Você é um assistente virtual chamado João."},
    {"role": "system", "content": "Você responde perguntas de compradores de imoveis. Se o contexto da conversa fugir este tema despeça educadamente."},
    {"role": "system", "content": "Você é um assistente útil e amigável."}
]

messages_dict = {}


# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nome = update.effective_user.first_name or "amigo(a)"
    await update.message.reply_text(f"Olá, {nome}! 🤖 Use /help para ver os comandos.")



# mensagens comuns (sem comando)
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id  = update.message.chat.id
    user_input = update.message.text

    if user_id not in messages_dict:
        messages_dict[user_id] = messages[:]

    messages_obj = messages_dict[user_id]

    # Adiciona a mensagem do usuário ao histórico
    messages_obj.append({"role": "user", "content": user_input})

    # Envia para a API
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Pode trocar para "gpt-4.1", etc.
        messages=messages_obj
    )

    # Captura a resposta
    reply = response.choices[0].message.content

    # Adiciona a resposta ao histórico
    messages_obj.append({"role": "assistant", "content": reply})

    print(f"ChatGPT: {reply}\n")


    await update.message.reply_text(reply)


def main() -> None:
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
    # chat()
