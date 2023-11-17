import os
from io import BytesIO
from queue import Queue
import requests
from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from bs4 import BeautifulSoup
# script_principal.py
from config import TOKEN, URL
# Avant
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Dispatcher

# Après
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Dispatcher
from telegram.ext.filters import FILTERS


TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
bot = Bot(TOKEN)

api_key = "3934b457b5c66f9c74c05ee2cf414419267ab8cb"
url_list = {}

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
    try:
        movies_list = []
        movies_details = {}
        website = BeautifulSoup(requests.get(f"https://mkvcinemas.skin/?s={query.replace(' ', '+')}").text, "html.parser")
        movies = website.find_all("a", {'class': 'ml-mask jt'})
        
        for movie in movies:
            if movie:
                movies_details["id"] = f"link{movies.index(movie)}"
                movies_details["title"] = movie.find("span", {'class': 'mli-info'}).text
                url_list[movies_details["id"]] = movie['href']
            
            movies_list.append(movies_details)
            movies_details = {}

        return True, movies_list  # Indique que l'opération a réussi et renvoie la liste des films
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None  # Indique que l'opération a échoué et renvoie None pour la liste des films

# Exemple d'utilisation :
success, movies_list = search_movies('your_query')
if success:
    print(f"Movies list: {movies_list}")
else:
    print("Failed to search movies.")


def get_movie(query, api_key):
    try:
        movie_details = {}
        movie_page_link = BeautifulSoup(requests.get(f"{url_list[query]}").text, "html.parser")
        
        title = movie_page_link.find("div", {'class': 'mvic-desc'}).h3.text
        movie_details["title"] = title
        img = movie_page_link.find("div", {'class': 'mvic-thumb'})['data-bg']
        movie_details["img"] = img
        links = movie_page_link.find_all("a", {'rel': 'noopener', 'data-wpel-link': 'internal'})
        
        final_links = {}
        for i in links:
            url = f"https://urlshortx.com/api?api={api_key}&url={i['href']}"
            response = requests.get(url)
            link = response.json()
            final_links[f"{i.text}"] = link['shortenedUrl']
        
        movie_details["links"] = final_links
        return True, movie_details  # Indique que l'opération a réussi et renvoie les détails du film
    except Exception as e:
        print(f"An error occurred: {e}")
        return False, None  # Indique que l'opération a échoué et renvoie None pour les détails du film

# Exemple d'utilisation :
success, movie_details = get_movie('your_query', 'your_api_key')
if success:
    print(f"Movie details: {movie_details}")
else:
    print("Failed to get movie details.")

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
  
