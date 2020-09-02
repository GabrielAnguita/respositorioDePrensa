#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from datetime import datetime as dt
from datetime import date, timedelta

import pymongo
import spacy
import re
from collections import Counter


# In[2]:


nlp = spacy.load("es_core_news_lg")


# In[3]:


def noticias_mercurio_dia(año, mes, dia):
    start = dt(año, mes, dia, 0, 0, 0)
    end = start + timedelta(1)

    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["noticias"]
    collection = db["mercurio_raw"]
    noticias_mercurio = [noticia for noticia in collection.find(
        {'fechaPublicacion': {'$lt': end, '$gte': start}})]
    return noticias_mercurio


# In[24]:


def noticias_mostrador_dia(año, mes, dia):
    start = dt(año, mes, dia, 0, 0, 0)
    end = start + timedelta(1)
    client = pymongo.MongoClient("mongodb://localhost:27017")
    db = client["noticias"]
    collection = db["mostrador_raw"]
    noticias_mostrador = [noticia for noticia in collection.find(
        {'fecha publicacion': {'$lt': end, '$gte': start}})]
    return noticias_mostrador


# In[5]:


# In[6]:


# In[11]:


# In[7]:


palabras_pegadas = re.compile(r"\S+\.[^a-z\s]")

def agrega_espacios(match):
    return match.group().replace(".", ". ")


def doc_mercurio(noticias):
    text = " ".join([(noticia["titulo"] + " " + noticia["bajada"] + " " +
                      noticia["texto"]).replace(u'\xa0', u' ') for noticia in noticias])
    text = re.sub(palabras_pegadas, agrega_espacios, text)
   
    doc = nlp(text)
    return doc


def doc_mostrador(noticias):
    text = " ".join([(noticia["titulo"] + " " + noticia["bajada"] + " " +
                      noticia["cuerpo"]).replace(u'\xa0', u' ') for noticia in noticias])
    text = re.sub(palabras_pegadas, agrega_espacios, text)
 
    doc = nlp(text)
    return doc

# In[8]:


# In[9]:


def common_proper_nouns(document):
    importantes = ["PROPN"]
    lemas = [w.lemma_ for w in document if w.pos_ in importantes]
    cuontalemas = Counter(lemas)
    cuenta = Counter.most_common(cuontalemas)
    return [[k,v] for (k, v) in cuenta]


# In[10]:


def common_nouns(document):
    importantes = ["NOUN"]
    lemas = [w.lemma_ for w in document if w.pos_ in importantes]
    cuontalemas = Counter(lemas)
    cuenta = Counter.most_common(cuontalemas)
    return [[k,v] for (k, v) in cuenta]


# In[11]:


def common_verbs(document):
    importantes = ["VERB"]
    lemas = [w.lemma_ for w in document if w.pos_ in importantes]
    cuontalemas = Counter(lemas)
    cuenta = Counter.most_common(cuontalemas)
    return [[k,v] for (k, v) in cuenta]


# In[ ]:


# In[26]:


def inserta_cuentas_mostrador(dia):
    collection = db["cuenta_mostrador_prueba10"]
    if (dia_most := noticias_mostrador_dia(dia.year, dia.month, dia.day)):
        doc = doc_mostrador(dia_most)
        prop_nouns = common_proper_nouns(doc)
        nouns = common_nouns(doc)
        verbs = common_verbs(doc)
        collection.insert_one({"dia": str(dia), "cuentas": {
                              "sustantivos_comunes": nouns, "sustantivos_propios": prop_nouns, "verbos": verbs}},
                              bypass_document_validation=True)


# In[27]:


def inserta_cuentas_mercurio(dia):
    collection = db["cuenta_mercurio_prueba10"]
    if (dia_merc := noticias_mercurio_dia(dia.year, dia.month, dia.day)):
        doc = doc_mercurio(dia_merc)
        prop_nouns = common_proper_nouns(doc)
        nouns = common_nouns(doc)
        verbs = common_verbs(doc)
        collection.insert_one({"dia": str(dia), "cuentas": {
                              "sustantivos_comunes": nouns, "sustantivos_propios": prop_nouns, "verbos": verbs}},
                              bypass_document_validation=True)


# In[ ]:


# In[28]:

# esta función nos hace fácil iterar a traves de fechas
def rango_fechas(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


fecha_inicio = dt(2020, 4, 1)
fecha_fin = dt(2020, 8, 5)

client = pymongo.MongoClient("mongodb://localhost:27017")
db = client["noticias"]

for dia in rango_fechas(fecha_inicio, fecha_fin):
    inserta_cuentas_mostrador(dia)
    inserta_cuentas_mercurio(dia)


# In[13]:
