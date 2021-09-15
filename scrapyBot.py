#!/usr/bin/env python
# pylint: disable=C0116,W0613

import logging
from os import replace
from typing import DefaultDict, Pattern

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient
import time

##Sitios
sites= ["pagina","clarin","nacion"]
##Secciones
sections= ["politica","economia","deportes","mundo"]

#Connect Mongodb atlas database
client = MongoClient("mongodb+srv://scrapy:$cr4Py!@cluster0.m4phb.mongodb.net/scrapynews?retryWrites=true&w=majority")
db = client.get_database('scrapynews')
news = db.news


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    user = update.message.chat.first_name
    message = "¡Hola <b>"+user+"</b>!\nPara pedir noticias tenes que escribir:  \n"\
        "     ---------------------------------------------------------\n"\
        "         <b>sitio seccion cantidad</b>(<i>opcional</i>) \n"\
        "     ---------------------------------------------------------\n"\
        "<u>Ejemplos:</u>\nSi queremos la ultima noticia de politica del diario <b>Clarin</b> escribimos:\n\n"\
            "<b>        clarin politica</b>\n\nSi queremos las ultimas dos noticias de deportes de <b>Pagina 12</b> escribimos:\n\n<b>        pagina deportes 2</b>\n\n"\
        "El limite de noticias es 10\n\n"\
         "Para mas información escribi comando /help\n\n"\
        "<b><i>ScrapyNews</i></b>"
    update.message.reply_text(message,parse_mode='HTML')

    

def help_command(update: Update, context: CallbackContext) -> None:
    message = "<b>SITIOS</b>        |   <b>COMANDO</b> \nClarin          |   clarin \nPagina 12  |   pagina\nLa Nación  |   nacion\n"\
        "<b>SECCIONES</b>: \nPolitica Deportes Economia Mundo"
    update.message.reply_text(message,parse_mode='HTML')



def normalize(s):
    replacements = (("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"))
    for a, b in replacements:
        s = s.replace(a,b).replace(a,b)
    return s


def query(update,context):
    msg = normalize(update.message.text.lower()).split()
    wrong_query = lambda x: False if len(msg) not in range(2,4) else (True if (msg[0] in sites) and (msg[1] in sections) else False ) 
    if wrong_query(msg):
        message = 'Buscando noticias para vos <b>'+update.message.chat.first_name+'</b> ...'
        update.message.reply_text(message,parse_mode='HTML')
        limit = lambda x: 1 if len(x)<3 else (1 if int(x[2]) not in range(1,10) else int(x[2]))
        return news.find({"site":msg[0],"section":msg[1],"last":{"$gte":0}}).sort([("last",-1),("_id",1)]).limit(limit(msg))
    else:
        message= "<i>'"+update.message.text +"' </i> no es un comando valido"
        update.message.reply_text(message,parse_mode='HTML')
        help_command(update,context)
        return []



def getNews(update,context):
    data = query(update,context)
    for x in data:
        message = '<a href="'+ x['url']+'">' + x['title']+' </a>'
        update.message.reply_text(message,parse_mode='HTML')

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = "1990069718:AAGz3WDQVNBc-z6bMLH0Wf8WzKMUwcKamho"
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, getNews))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
