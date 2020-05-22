#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 19:14:34 2020

@author: wandita
"""

import requests
from bs4 import BeautifulSoup as bs

import re

class noticia_mostrador:
    def __init__(self, titulo, url, bajada, cuerpo,
                 fecha_publicacion, fecha_edicion, relacionadas, tags=None,
                 categoria=None, autor=None, ide=None):
        
        
        self.ide = ide
        self.titulo = titulo
        self.bajada = bajada
        self.cuerpo = cuerpo
        self.tags = tags
        self.categoria = categoria
        self.autor = autor
        self.url = url
        self.fecha_publicacion = fecha_publicacion
        self.fecha_edicion = fecha_edicion
        self.relacionadas = relacionadas
    
    def to_dict(self):
        
        return {"titulo":self.titulo,
                "bajada":self.bajada,
                "cuerpo":self.cuerpo,
                "tags":self.tags,
                "categoria":self.categoria,
                "autor":self.autor,
                "url":self.url,
                "fecha publicacion":self.fecha_publicacion,
                "fecha edicion":self.fecha_edicion,
                "relacionadas":self.relacionadas}
        
def scrape_noticia(url, ide=None):
       
    with requests.Session() as s:
        respuesta = s.get(url)
    html = respuesta.text
    sopa = bs(html, 'html.parser')
    
        
    if sopa.find("h2", {"class":"titulo-single"}) is not None:
        titulo = sopa.find("h2", {"class":"titulo-single"}).text.strip()
    
    elif sopa.find("div",{"class":"avatar-y-titulo"}).find("h2") is not None:
        titulo = sopa.find("div",{"class":"avatar-y-titulo"}).find("h2").text.strip()
        
    bajada = sopa.find("figcaption").text.strip()
    
    cuerpo_trozado = sopa.find("div",{"class":"cuerpo-noticia"}).findAll(["p","h1","h2","h3","ul","ol"])
    
    cuerpo = []
    for trozo in cuerpo_trozado:
    
        if trozo.name in ["ul","ol"]:
            for item in trozo.findAll("li"):
                cuerpo.append((item.text, item.name))
        else:
            cuerpo.append((trozo.text, trozo.name))
            
        
       
    tags =  [tag["content"].lower() for tag in sopa.findAll("meta",{"property":"article:tag"})]
    
    categoria = sopa.find("meta",{"property":"article:section"})["content"]
   
    autor =  (sopa.find("a",{"rel":"author"}).text, sopa.find("a",{"rel":"author"})["href"])
      
    fecha_publicacion = sopa.find("meta",{"property":"article:published_time"})["content"]
    
    if fecha_publicacion is None:
        formato_fecha = re.compile('\d{4}/\d{2}/\d{2}')
        fecha_publicacion = formato_fecha.search(url).group()
    
    fecha_edicion = sopa.find("meta",{"property":"article:modified_time"})["content"]
    
    relacionadas = [link["href"] for link in sopa.find("section",{"class":"noticias-relacionadas"}).findAll("a",{"class":"ver-mas"})]
    
    noticia = noticia_mostrador(titulo = titulo,
                                bajada = bajada,
                                cuerpo = cuerpo,
                                tags = tags,
                                categoria = categoria,
                                autor = autor,
                                url = url,
                                ide = ide,
                                fecha_publicacion = fecha_publicacion,
                                fecha_edicion = fecha_edicion,
                                relacionadas = relacionadas)
    
    return noticia
    

