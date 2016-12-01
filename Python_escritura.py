#Definicion modulo RE
import re;
import MySQLdb

import urllib2
import urllib
from urllib import urlopen

#Importar libreria time (Recoger datos cada 2 minutos)
import time

#Importar el modulo Flask y crear una app
from flask import Flask, render_template
#Importar el modulo request para almacenar umbral del formulario POST
from flask import request, Response, jsonify

import ast
import json

#Definicion de modulo Thing Speak
import thingspeak

#SSE

# Make sure your gevent version is >= 1.0




while True:
	
	import time
	to_wait = -(time.time()%120)+120
	time.sleep(to_wait)
	# time.sleep(10)	

	
	#Poner URL de la empresa seleccionada para estudiar la cotizacion
	url = urllib.urlopen("http://www.infobolsa.es/cotizacion/grafico-b.popular")
	#Se almacena todo el codigo fuente de pagina "http://www.infobolsa.es/"
	data = url.read()
	

	#Para almacenar todas las FECHAS de codigo fuente
	date = re.findall(r'(\d{2}\/\d{2}\/\d{4})',data);

	#Para extraer e imprimir la primera fecha
	date0 = date[0];
	################################################################
	#Para almacenar todas las HORAS de codigo fuente
	time = re.findall(r'(\d{2}:\d{2})',data);

	#Para extraer e imprimir la primera hora
	time0 = time[0];

	################################################################
	#Para almacenar todas las COTIZACIONES de codigo fuente
	price = re.findall(r'(\d{1},\d{3})',data);
	
	price_float=float(str(price[0]).replace(",", "."))

	#Para extraer e imprimir la primera hora
	price0 = price_float;
	
	urllib.urlopen("https://api.thingspeak.com/update?api_key=470WJU9MI5PGK4J1&field1="+str(price0))
	
	db = MySQLdb.connect(host="localhost",user="phpmyadmin",passwd="hogar",db="bolsa_db")
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursor.execute("INSERT INTO C (Precio,Tiempo,Fecha) VALUES (%s,%s,%s)",((price0),time0,date0))
	print price0
	
	db.commit()
	# disconnect from server
	cursor.close()
	db.close()
	
	
	
