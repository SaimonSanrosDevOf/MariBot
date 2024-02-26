import telebot
import google.generativeai as genai
import config
import string

# Configurar a API do Google
genai.configure(api_key=config.GOOGLE_API_KEY)

# Inicializar o bot do Telegram
bot = telebot.TeleBot(config.TELEGRAM_TOKEN)

# Encontrar o modelo suportado
model_name = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        model_name = m.name
        break

# Iniciar o modelo
model = genai.GenerativeModel(model_name)
chat = model.start_chat(history=[])

# Dicionário para armazenar o nome dos usuários
user_names = {}

# Manipulador de mensagens
@bot.message_handler(func=lambda message: True)
def respond_to_message(message):
    global user_names
    
    # Obter o primeiro nome do usuário
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    
    # Armazenar o nome do usuário se ainda não estiver armazenado
    if user_id not in user_names:
        user_names[user_id] = user_first_name
        
    # Responder ao usuário
    response = chat.send_message(message.text)
    template = string.Template(response.text)
    formatted_response = template.substitute(name=user_names[user_id])
    bot.reply_to(message, formatted_response)

# Iniciar o bot
bot.polling()
