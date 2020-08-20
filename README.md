# tantiandolaprensy
Este proyecto está en proceso, de lo que se trata es de llevar un registro de lo que se publica en 2 sitios chilenos de prensa online para luego hacer un minimo analisis del contenido. Por ahora solo cuento palabras por día y quisiera generar una api a la que acceder para poder visualizar desde otra aplicacion gráficos que muestren la importancia de las temáticas, nombres, o conceptos, segun la fecha que uno quiera ver. 

El texto se obtiene haciendo scraping de esos sitios con python y se guarda en mongo DB. Se usa Spacy para tokenizar el texto y asi poder contar palabras. Luego se guarda la información ya procesada en Mongo, y se expone a través de una app de Flask. Se agradecen ideas y criticas!
