#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 20:10:26 2020

@author: wandita
"""

import socks
import requests
import socket
from bs4 import BeautifulSoup as bs
import json
import time
import re
import pymongo
from datetime import datetime as dt
from plantillas import succionador_mercurial, noticia_mostrador


# Not sure if this has any significance, but does no harm

headers = { "Host": "cache-elastic-pandora.ecn.cl",
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Origin": "https://www.emol.com",
"Connection": "keep-alive",
"Referer": "https://www.emol.com/todas/" }


# returns anonymous requests session (needs tor enabled)
def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


# EL MERCURIO SECTION #

url_mercurio = "AQUI VA LA URL DE LA API, ENCUENTRELA USTED"



# Open connection to our DB for storing the news
client = pymongo.MongoClient("mongodb://localhost:27017")
# choose a database
db = client["noticias"]
# and then a collection
collection = db["mercurio_raw"]

for i in range(0,100):
    
    noticias_mercurio = [] 
    # should create new requests session, for resetting tor proxy (does not really work yet)
    session = get_tor_session()
    
    # Check if ip is properly hidden
    print(session.get("http://httpbin.org/ip").text)

    # response object from querying the API 
    response = session.get(url_mercurio + str( i*30 ), headers=headers)
    
    # Fills list with parsed news from response
    noticias_mercurio += succionador_mercurial(response)
    print(f"{len(noticias_mercurio)} noticias en ram")
        
    # ...
    for noticia in noticias_mercurio:
        print("Archivando en bd: " + noticia["url"])
        
        collection.insert_one(noticia)
    
    # A timer shows respect
    time.sleep(0.3)
    


# END OF EL MERCURIO SECTION #



# EL MOSTRADOR SECTION # 
url_mostrador = "https://www.elmostrador.cl/destacado/"


# we will use different collections for storing from different sources
collection = db["mostrador_raw"]
# Go through 'destacado' section for collecting links

for i in range(1,100):
    queue = []
    time.sleep(0.3)
    
    if i > 1:
        res = requests.get(url_mostrador + "page/" + str(i) + "/")
    else:
        res = requests.get(url_mostrador)
    print(res)
    print(i)
    html_text = res.text
    soup = bs(html_text, "html.parser")
    links = [link.a["href"] for link in soup.find("section",{"class":"lo-ultimo"}).findAll("h4") if link.a["href"] not in queue]
    queue += links

    for link in queue:
        print("Archivando: " + link)
        time.sleep(0.1)    
        session = get_tor_session()
        response = session.get(link)
        noticia = noticia_mostrador(response=response, url=link)
        collection.insert_one(noticia)



