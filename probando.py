#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:36:09 2020

@author: wandita
"""

import requests
from bs4 import BeautifulSoup as bs
import re

url ="https://www.elmostrador.cl/destacado/2020/05/10/la-hora-de-lo-publico-coordenadas-para-la-oposicion/"


with requests.Session() as s:
    respuesta = s.get(url)

texto = respuesta.text
sopa = bs(texto, 'html.parser')



if sopa.find("h2", {"class":"titulo-single"}) is not None:
    titulo = sopa.find("h2", {"class":"titulo-single"}).text.strip()

elif sopa.find("div",{"class":"avatar-y-titulo"}).find("h2") is not None:
    titulo = sopa.find("div",{"class":"avatar-y-titulo"}).find("h2").text.strip()

autor = (sopa.find("a",{"rel":"author"}).text, sopa.find("a",{"rel":"author"})["href"])
 
fecha_publicacion = sopa.find("meta",{"property":"article:published_time"})["content"]

if fecha_publicacion is None:
    formato_fecha = re.compile('\d{4}/\d{2}/\d{2}')
    fecha_publicacion = formato_fecha.search(url).group()

fecha_edicion = sopa.find("meta",{"property":"article:modified_time"})["content"]

seccion = sopa.find("meta",{"property":"article:section"})["content"]

tags = [tag["content"].lower() for tag in sopa.findAll("meta",{"property":"article:tag"})]

relacionadas = [link["href"] for link in sopa.find("section",{"class":"noticias-relacionadas"}).findAll("a",{"class":"ver-mas"})]

cuerpo_trozado = sopa.find("div",{"class":"cuerpo-noticia"}).findAll(["p","h1","h2","h3","ul","ol"])

cuerpo = []
for trozo in cuerpo_trozado:

    if trozo.name in ["ul","ol"]:
        for item in trozo.findAll("li"):
            cuerpo.append((item.text, item.name))
    else:
        cuerpo.append((trozo.text, trozo.name))
        