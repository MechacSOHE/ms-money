import os
from io import BytesIO
from queue import Queue
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher
from bs4 import BeautifulSoup
# script_principal.py
from config import TOKEN, URL

TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
bot = Bot(TOKEN)

api_key = "3934b457b5c66f9c74c05ee2cf414419267ab8cb"
url_list = {}

def welcome(update, context) -> None:
def search_and_reply(query, chat_id):
    try:
        movies_list = search_movies(query)
        if movies_list:
            keyboards = []
            for movie in movies_list:
                keyboard = InlineKeyboardButton(movie["title"], callback_data=movie["id"])
                keyboards.append([keyboard])
            reply_markup = InlineKeyboardMarkup(keyboards)
            bot.send_message(chat_id, 'Search Results...', reply_markup=reply_markup)
        else:
            bot.send_message(chat_id, 'Sorry 🙏, No Result Found!\nCheck If You Have Misspelled The Movie Name.')
    except Exception as e:
        print(f"An error occurred: {e}")
        bot.send_message(chat_id, 'An error occurred while processing your request. Please try again later.')

# ... (le reste de votre code actuel)

def search_movies(query):
    # ... (votre code actuel)

def get_movie(query, api_key):
    # ... (votre code actuel)

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/{}'.format(TOKEN), methods=['GET', 'POST'])
def respond():
    update = Update.de_json(request.get_json(force=True), bot)
    setup().process_update(update)
    return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
@app.route('/search_movie', methods=['POST'])
def search_movie_route():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    query = data['message']['text']
    search_and_reply(query, chat_id)
    return 'ok'

@app.route('/get_movie_details', methods=['POST'])
def get_movie_details_route():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    query = data['message']['text']
    get_movie_details(query, chat_id)
    return 'ok'
  
