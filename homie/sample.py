import telebot


bot = telebot.TeleBot('<telegram-token>')
@bot.message_handler(commands=['start'])
def start_command(message):
    print(message.chat.id)
    print(message.chat.id)
