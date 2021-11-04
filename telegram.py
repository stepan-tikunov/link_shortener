from telebot import TeleBot
from json import loads
from re import match
from models import Link, db

with open("config.json") as f:
    config = loads(f.read())

bot = TeleBot(config["TELEGRAM_BOT_TOKEN"])

@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.reply_to(message, "Пришли ссылку")

@bot.message_handler(content_types=["text"])
def link_handler(message):
    url = None
    print(message.entities)
    for entity in message.entities or []:
        print(entity)
        if entity.type == "url":
            url = message.text[entity.offset:entity.offset + entity.length]
        if entity.type == "text_link":
            url = entity.url
    print(url is None)
    if url:
        if not match(r"https?://", url):
            url = "http://" + url
        link = Link(url)
        db.session.add(link)
        db.session.commit()
        host = config["HOST"]
        bot.reply_to(message, f"https://{host}/{link.id}")
    else:
        bot.reply_to(message, "В этом сообщении нет ссылок")
