from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

import os
# 🔹 Inicializa o cliente OpenAI
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # Lê a chave da variável de ambiente
)

# 🔹 Token do seu bot do Telegram
TOKEN = '8432091505:AAEsalHlwgAPGUY_k92NW7iqaj3fB9WH8Co'
USER = '@meu_bot_magic_bot'

# 🔹 Mensagens padrão do sistema
messages = [
    {"role": "system", "content": "Você é um assistente virtual chamado João Boleiro."},
    {"role": "system", "content": "Você responde perguntas de futebol. Se o contexto da conversa fugir deste tema despeça educadamente."},
    {"role": "system", "content": "Você é um assistente útil e amigável."}
]

# 🔹 Dicionário para manter histórico de cada usuário
messages_dict = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_user or not update.message:
        return

    nome = update.effective_user.first_name or "amigo(a)"
    await update.message.reply_text(f"Olá, {nome}! 🤖 Use /help para ver os comandos.")

# mensagens comuns (sem comando)
async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # garante que temos message e texto
    if not update.message or not update.message.text:
        return

    user_id = update.message.chat.id
    user_input = update.message.text

    if user_id not in messages_dict:
        messages_dict[user_id] = messages[:]  # cópia inicial

    messages_obj = messages_dict[user_id]

    # adiciona mensagem do usuário ao histórico
    messages_obj.append({"role": "user", "content": user_input})

    # chama a API da OpenAI com tratamento de erros
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages_obj
        )
        reply = response.choices[0].message.content or "⚠️ Sem resposta da OpenAI."
    except Exception as e:
        reply = f"⚠️ Ocorreu um erro: {e}"

    # adiciona resposta ao histórico
    messages_obj.append({"role": "assistant", "content": reply})

    print(f"ChatGPT: {reply}\n")

    await update.message.reply_text(reply)

# main
def main() -> None:
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
