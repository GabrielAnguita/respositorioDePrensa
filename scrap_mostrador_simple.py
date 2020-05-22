#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:14:34 2020

@author: wandita
"""

import requests
from bs4 import BeautifulSoup as bs

import re


        
def scrape_noticia(url, ide=None):
       
    with requests.Session() as s:
        respuesta = s.get(url)
    html = respuesta.text
    sopa = bs(html, 'html.parser')
    
    try:    
        if sopa.find("h2", {"class":"titulo-single"}) is not None:
            titulo = sopa.find("h2", {"class":"titulo-single"}).text.strip()
        
        elif sopa.find("div",{"class":"avatar-y-titulo"}) is not None:
            titulo = sopa.find("div",{"class":"avatar-y-titulo"}).find("h2").text.strip()
        
        elif sopa.find("meta",{"itemprop":"name"}) is not None:
 
            titulo = sopa.find("meta",{"itemprop":"name"})["content"]
    
    except:
        titulo = "NINGUNO"         
    
    try:
        bajada = sopa.find("figcaption").text.strip()
    except:
        bajada = "NINGUNO"
    
    try:
        cuerpo_trozado = sopa.find("div",{"class":"cuerpo-noticia"}).findAll(["p","h1","h2","h3","ul","ol"])
        
        cuerpo = []
        for trozo in cuerpo_trozado:
        
            if trozo.name in ["ul","ol"]:
                for item in trozo.findAll("li"):
                    cuerpo.append((item.text, item.name))
            else:
                cuerpo.append((trozo.text, trozo.name))
    except:
        cuerpo = "NINGUNO"             
        
    try:   
        tags =  [tag["content"].lower() for tag in sopa.findAll("meta",{"property":"article:tag"})]
    except:
        tags = "NINGUNO"
        
    try:
        categoria = sopa.find("meta",{"property":"article:section"})["content"]
    except:
        categoria = "NINGUNO"
    
    try:
        autor =  (sopa.find("a",{"rel":"author"}).text, sopa.find("a",{"rel":"author"})["href"])
    except:
        autor = "NINGUNO"
    
        
    try:
        fecha_publicacion = sopa.find("meta",{"property":"article:published_time"})["content"]
        
        if fecha_publicacion is None:
            formato_fecha = re.compile('\d{4}/\d{2}/\d{2}')
            fecha_publicacion = formato_fecha.search(url).group()
    except:
        fecha_publicacion = "NINGUNO"
        
    try:
        fecha_edicion = sopa.find("meta",{"property":"article:modified_time"})["content"]
    except:
        fecha_edicion = "NINGUNO"
    
    try:
        relacionadas = [link["href"] for link in sopa.find("section",{"class":"noticias-relacionadas"}).findAll("a",{"class":"ver-mas"})]
    except:
        relacionadas = "NINGUNO"
    
    noticia =  {"titulo":titulo,                       # string
                "bajada":bajada,                       # string
                "cuerpo":cuerpo,                       # lista de tuplas (string, string)
                "tags":tags,                           # lista de string
                "categoria":categoria,                 # string
                "autor":autor,                         # tupla de strings (nombre, url)
                "url":url,                             # string
                "fecha publicacion":fecha_publicacion, # string
                "fecha edicion":fecha_edicion,         # string
                "relacionadas":relacionadas}           # lista de strings
    
    return noticia
    