import telebot
import json
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time, requests
from bs4 import BeautifulSoup

# Token do bot
with open('config.json', 'r') as file:
        config = json.loads(file.read())
        token = config['token']
        apichk = config["api"]
        # Coloque o @ no user do bot
        userBot = config["userBot"]
        chat_idDono = config["chat_idDono"]
        url = config["url_postgres"]
        
bot = telebot.TeleBot(token)

# Inline botão
markup = InlineKeyboardMarkup()
markup.row_width = 1
markup.add(InlineKeyboardButton("💳 DONO DO BOT", url="https://t.me/marcolasdc"),InlineKeyboardButton("💳 DONO DO CHK", url="https://t.me/marcolasdc"))

# comandos /menu e /start
@bot.message_handler(commands=["start", "menu"])
def menu(message):
  bot.reply_to(message, "Digite /chk para fazer o checker das suas ccs!")

# comando do chk
@bot.message_handler(commands=["chk"])
def chk(message):
  if message.chat.type == "private":
    bot.send_message(message.chat.id, "Só funciono em grupos!")
  else:
    if message.text == "/chk":
      bot.send_message(message.chat.id, "*Chk Full Zero Auth, Digite /chk cartao|mes|ano|cvv*", parse_mode="MARKDOWN")
    elif message.text == f"/chk{userBot}":
      bot.send_message(message.chat.id, "*Chk Full Zero Auth, Digite /chk cartao|mes|ano|cvv*", parse_mode="MARKDOWN")
    else:
      msg = bot.reply_to(message, "*Aguarde...*", parse_mode="MARKDOWN")
      time.sleep(6)
      cc = message.text.split("/chk ")[1]
      data = requests.post(apichk+cc).text
      # retirando tags html
      cleantext = BeautifulSoup(data, "html.parser").text
      bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=(cleantext), reply_markup=markup)
bot.infinity_polling()