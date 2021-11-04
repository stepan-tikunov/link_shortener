from flask import Flask, abort, redirect, request
from telebot.types import Update
from telegram import bot
from models import db, Link
from json import loads

with open("config.json") as f:
    config = loads(f.read())

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = config["DATABASE_URI"]

db.init_app(app)
db.app = app

@app.route("/bot/<token>", methods=["POST"])
def webhook(token):
    if token == bot.token:
        bot.process_new_updates([Update.de_json(request.data.decode("utf-8"))])
    
    return 'ok'

@app.route("/<short_url>")
def redirect_to_full_link(short_url):
    link = Link.query.get(short_url)

    if link:
        return redirect(link.full_link)
    
    abort(404)

if __name__ == "__main__":
    app.run("0.0.0.0", 8000)
