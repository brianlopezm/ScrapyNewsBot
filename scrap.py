from bs4 import BeautifulSoup
from pymongo import MongoClient
from itertools import islice
import requests
import json


client = MongoClient("mongodb+srv://scrapy:$cr4Py!@cluster0.m4phb.mongodb.net/scrapynews?retryWrites=true&w=majority")
db = client.get_database('scrapynews')
news = db.news


#Crea una noticia -> Es un diccionario
def createNews(sitio,seccion,titulo,url):
    noticia = {
        'title': titulo,
        'url':url,
        'site': sitio,
        'section': seccion,
        'last':1 #1 es el ultimo, 0 el anteultimo y -1 listo para borrar
    }
    news.insert_one(noticia)

def scrap(obj,titSoup): #a partir de lista de tags,scrapeamos la noticia y sacamos titulo y link.
    for tit in islice(titSoup,0,10): #Tratamos de que no traiga mas que 10 noticias
        title = tit.find(obj['title'])
        if title:
            titulo = title.text.strip()
            link = tit.find(obj['link'])
            if link:
                url= obj['rootURL']+link.attrs.get(obj['attlink'])
                createNews(obj['site'],obj['section'],titulo,url)


#Dada una url  toma todos los tags indicados y por cada uno scrapea la cada una de las noticias
def getSoup(obj):
    page = requests.get(obj['fullURL'])
    soup = BeautifulSoup(page.content,"html.parser")
    tagsList = obj['tags']
    for tag in tagsList:
        scrap(obj,soup.find_all(tag))

#Obtiene info de la BD para scrapear
def load():
    with open('data.json','r',encoding='utf-8') as json_file:
        return json.load(json_file)


def main():
    print("Recuperando info de scrap...")
    json_data = load()
    print("Realizando cambios en la base de datos...")
    news.update_many({"last":0},{"$set":{"last":-1}})
    news.update_many({"last":1},{"$set":{"last":0}})
    print("Scrapeando....")
    for obj in json_data:
        getSoup(obj)
    print("Eliminando noticias desactualizadas...")
    news.delete_many({"last":-1})
    

if __name__ == '__main__':
    main()