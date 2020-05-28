#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:14:34 2020

@author: wandita
"""

import requests
from bs4 import BeautifulSoup as bs
import json

import re

headers = { "Host": "cache-elastic-pandora.ecn.cl",
"Accept": "application/json, text/javascript, */*; q=0.01",
"Accept-Language": "en-US,en;q=0.5",
"Accept-Encoding": "gzip, deflate, br",
"Origin": "https://www.emol.com",
"Connection": "keep-alive",
"Referer": "https://www.emol.com/todas/" }

url = "https://cache-elastic-pandora.ecn.cl/emol/noticia/_search?q=publicada:true+AND+ultimoMinuto:true+AND+seccion:*+AND+temas.id:*&sort=fechaModificacion:desc&size=30&from=30"

response = requests.get(url, headers=headers)
  
payload = json.loads(response.text)

lista_noticias = []

cleanr = re.compile('{.*?}')

 


for noticia in payload["hits"]["hits"]:
    texto = bs(noticia["_source"]["texto"], "html.parser").text
    textolimpio = re.sub(cleanr, '', texto)  
    
    noti = {}
    noti["id"] = noticia["_id"]
    noti["autor"] = noticia["_source"]["autor"]
    noti["fuente"] = noticia["_source"]["fuente"]
    noti["seccion"] = noticia["_source"]["seccion"]
    noti["subSeccion"] = noticia["_source"]["subSeccion"]
    noti["fechaModificacion"] = noticia["_source"]["fechaModificacion"]
    noti["fechaPublicacion"] = noticia["_source"]["fechaPublicacion"]
    noti["temas"] = noticia["_source"]["temas"]
    noti["titulo"] = noticia["_source"]["titulo"]
    noti["bajada"] = noticia["_source"]["bajada"][0]["texto"]
    noti["texto"] = textolimpio
    noti["url"] = noticia["_source"]["permalink"]
    noti["tituloSEO"] = noticia["_source"]["tituloSEO"]
    noti["relevancia"] = noticia["_source"]["relevancia"]
    
    lista_noticias.append(noti)
  