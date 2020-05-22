#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  9 18:57:27 2020

@author: wandita
"""

import requests
from bs4 import BeautifulSoup as bs
import time
from scrap_mostrador_simple import scrape_noticia
from datetime import datetime
import csv


url = "https://www.elmostrador.cl/destacado/page/"


def add_links_to_queue(links, crawled_links):
    for link in links:
        if link in queue:
            continue
        if link in crawled_links:
            continue
        queue.append(link)
        

queue = []

crawled = open("/home/wandita/Documents/Programacion/proyectos/visualiza noticia/visited.txt", "r")
for i in range(1,20):
    time.sleep(1)
    response = requests.get(url+str(i))
    html_text = response.text
    soup = bs(html_text, "html.parser")
    links = [link.a["href"] for link in soup.find("section",{"class":"lo-ultimo"}).findAll("h4") if link.a["href"] not in queue]
    add_links_to_queue(links, crawled)

crawled.close()


with open("/home/wandita/Documents/Programacion/proyectos/visualiza noticia/visited.txt", "r") as visited:        
    visitadas = [line.split(',') for line in visited.readlines()]
    for link in queue:
        if link in visitadas:
            queue.remove(link)
   

headers = ["titulo","bajada","cuerpo","tags","categoria","autor","url","fecha publicacion", "fecha edicion","relacionadas"]
with open("/home/wandita/Documents/Programacion/proyectos/visualiza noticia/mostrador.csv", 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()


print(queue)
print(f"links en queue: {len(queue)}")

for link in queue:
    print("Archivando: " + link)
    time.sleep(1)
    noticia = scrape_noticia(link)
    with open("/home/wandita/Documents/Programacion/proyectos/visualiza noticia/mostrador.csv", 'a') as f:  # Just use 'w' mode in 3.x
        w = csv.DictWriter(f, noticia.keys(), delimiter='|')
        w.writerow(noticia)
   
    with open("/home/wandita/Documents/Programacion/proyectos/visualiza noticia/visited.txt", "a") as visited:        
        visited.write(link+"\n")

