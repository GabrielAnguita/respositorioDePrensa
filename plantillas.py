#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 20:10:26 2020

@author: wandita
"""

from bs4 import BeautifulSoup as bs
import json
import re
from datetime import datetime as dt


def succionador_mercurial(response):
    
    """
     Takes an http request response as argument, expects very precise json formatting inside of the response.
     Returns a list of dictionaries with relevant information for the news articles inside the http response
    """ 
      
    payload = json.loads(response.text)
    
    lista_noticias = []
    
   

    cleaner = re.compile('{.*?}')
    
     
    
    
    for noticia in payload["hits"]["hits"]:
        texto = bs(noticia["_source"]["texto"], "html.parser").text
        textolimpio = re.sub(cleaner, ' ', texto)  
        src = noticia["_source"]
        
        noti = {}
        noti["id"] = noticia["_id"]
        noti["autor"] = src["autor"]
        noti["fuente"] = src["fuente"]
        noti["seccion"] = src["seccion"]
        noti["subSeccion"] = src["subSeccion"]
        
        noti["fechaModificacion"] = dt.strptime(src["fechaModificacion"][:19], "%Y-%m-%dT%H:%M:%S")
        noti["fechaPublicacion"] = dt.strptime(src["fechaPublicacion"][:19], "%Y-%m-%dT%H:%M:%S")
        noti["temas"] = src["temas"]
        noti["titulo"] = src["titulo"]
        noti["bajada"] = src["bajada"][0]["texto"]
        noti["texto"] = textolimpio
        noti["url"] = src["permalink"]
        noti["tituloSEO"] = src["tituloSEO"]
        noti["relevancia"] = src["relevancia"]
        
        lista_noticias.append(noti)
        
    
    return lista_noticias


        
def noticia_mostrador(response, url):
 
    
    html = response.text
    sopa = bs(html, 'html.parser')
    
    # Título noticia    
    if sopa.find("h2", {"class":"titulo-single"}) is not None:
        titulo = sopa.find("h2", {"class":"titulo-single"}).text.strip()
    elif sopa.find("div",{"class":"avatar-y-titulo"}) is not None:
        titulo = sopa.find("div",{"class":"avatar-y-titulo"}).find("h2").text.strip()    
    elif sopa.find("meta",{"itemprop":"name"}) is not None:
        titulo = sopa.find("meta",{"itemprop":"name"})["content"]
    else:
        titulo = "NINGUNO"         
    
    #Bajada noticia
    if sopa.find("figcaption") is not None:
        bajada = sopa.find("figcaption").text.strip()
    else:
        bajada = "NINGUNO"
    
    #Cuerpo noticia
    if sopa.find("div",{"class":"cuerpo-noticia"}) is not None:
        cuerpo_trozado = sopa.find("div",{"class":"cuerpo-noticia"}).findAll(["p","h1","h2","h3","ul","ol"])
        
        cuerpo = ""
        for trozo in cuerpo_trozado:
        
            if trozo.name in ["ul","ol"]:
                for item in trozo.findAll("li"):
                    cuerpo += item.text
            else:
                cuerpo += trozo.text
    else:
        cuerpo = "NINGUNO"             


    #Tags    
    try:   
        tags =  [tag["content"].lower() for tag in sopa.findAll("meta",{"property":"article:tag"})]
    except:
        tags = "NINGUNO"

    #Categoria    
    try:
        categoria = sopa.find("meta",{"property":"article:section"})["content"]
    except:
        categoria = "NINGUNO"
    
    #Autor
    try:
        autor =  (sopa.find("a",{"rel":"author"}).text, sopa.find("a",{"rel":"author"})["href"])
    except:
        autor = "NINGUNO"
    
        
    
        
    fecha_publicacion = sopa.find("meta",{"property":"article:published_time"})
        
    if fecha_publicacion is None:
        formato_fecha = re.compile('\d{4}/\d{2}/\d{2}')
        fecha_publicacion = formato_fecha.search(url).group()
    
    else:
        fecha_publicacion = dt.strptime(fecha_publicacion["content"][:19], "%Y-%m-%dT%H:%M:%S")
    
    
        

    fecha_edicion = sopa.find("meta",{"property":"article:modified_time"})
    if fecha_edicion is None:
        fecha_edicion = "NINGUNO"
    else:
        fecha_edicion = dt.strptime(fecha_edicion["content"][:19], "%Y-%m-%dT%H:%M:%S")
    
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
    