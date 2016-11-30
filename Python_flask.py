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


app = Flask(__name__,)

GLO = time.time()
@app.route('/')
def index():

	return render_template('index.html')


@app.route('/hello/')
@app.route('/hello/<results1>')
def hello(name=None):
    return render_template('index.html', name=results1)	
	
###################################################################################
@app.route('/result1', methods=['POST'])
def result1():
	
	max = float(request.form['max_value'])
	
	#Se almacenan valores en matriz
	db = MySQLdb.connect(host="localhost",user="phpmyadmin",passwd="hogar",db="bolsa_db")
	cursor = db.cursor()
	cursor.execute("SELECT (Precio) FROM C")
	row = cursor.fetchone()	
	matrix = []
	i = 0
	while row is not None:
			matrix.append(row[0])
			row = cursor.fetchone()
			
	###########################################################################
	#Se debe fijar un porcentaje para el mensaje, para ello se introduce por boton de web
	value_th = matrix[0]
	price0 = matrix[-1]
	# last_result = lenght(matrix)

	
	sql = "select * from C"
	cursor.execute(sql)
	last_result=cursor.rowcount
	results = cursor.fetchall()
	#Valor actualizado
	results1 = results[-1]
	

	db.commit()
	# disconnect from server
	cursor.close()
	db.close()

	i = 0
	
	collected_data_max = []
	collected_data_min = []
	# matrix[2] = 1.2
	# matrix[3] = 1.3
	print last_result
	for i in range(0, last_result):
		# urllib.urlopen("https://api.thingspeak.com/update?api_key=470WJU9MI5PGK4J1&field1="+str(matrix[i]))
		a = 10
		if (matrix[i] <= ((1-max) * (value_th)) ):#0.84
			a = 0
			collected_data_min.append(matrix[i]) # Your data
		elif (matrix[i] >= ((1+max) * (value_th)) ):#0.86
			a = 1
			collected_data_max.append(matrix[i]) # Your data
			
		print i
	
		
	return jsonify(result_max=collected_data_max,result_min=collected_data_min)
	

@app.route('/graph', methods=['POST'])
def graph():

	#Se almacenan valores en matriz
	db = MySQLdb.connect(host="localhost",user="phpmyadmin",passwd="hogar",db="bolsa_db")
	cursor = db.cursor()
	cursor.execute("SELECT (Precio) FROM C")
	row = cursor.fetchone()	
	matrix = []

	while row is not None:
			matrix.append(row[0])
			row = cursor.fetchone()
			
	###########################################################################
	#Se debe fijar un porcentaje para el mensaje, para ello se introduce por boton de web
	value_th = matrix[0]
	price0 = matrix[-1]
	# last_result = lenght(matrix)

	
	sql = "select * from C"
	cursor.execute(sql)
	last_result=cursor.rowcount
	results = cursor.fetchall()
	#Valor actualizado
	results1 = results[-1]
	
	db.commit()
	# disconnect from server
	cursor.close()
	db.close()	
	
	# ch = thingspeak.Channel(196552)
	# ch.get({"channel":{"id":196552,"name":"Prize variation","description":"Complete afte","latitude":"0.0","longitude":"0.0","field1":"Field Label 1","created_at":"2016-11-29T08:10:31-05:00","updated_at":"2016-11-29T08:23:50-05:00"},"feeds": [22]})	
	

	

###########################################################################	

@app.route('/average',methods=['POST'])

def average():
	db = MySQLdb.connect(host="localhost",user="phpmyadmin",passwd="hogar",db="bolsa_db")
	cursor = db.cursor()
	cursor.execute("SELECT AVG(Precio) FROM C")
	row = cursor.fetchone()	
	p_average = row[0]

	return render_template('average.html',p_average = p_average)
	
@app.route('/load/')
def load():	
	while True:
		
		import time
		to_wait = -(time.time()%5)+5
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
		#return render_template('load.html')
		
@app.route('/thingspeak',methods=['POST'])
def thingspeak():	
	while True:
		

		
		#Poner URL de la empresa seleccionada para estudiar la cotizacion
		url = urllib.urlopen("http://www.infobolsa.es/cotizacion/grafico-b.popular")
		#Se almacena todo el codigo fuente de pagina "http://www.infobolsa.es/"
		data = url.read()
		

		# #Para almacenar todas las FECHAS de codigo fuente
		# date = re.findall(r'(\d{2}\/\d{2}\/\d{4})',data);

		# #Para extraer e imprimir la primera ti
		# date0 = date[0];
		# ################################################################
		# #Para almacenar todas las HORAS de codigo fuente
		# time = re.findall(r'(\d{2}:\d{2})',data);

		# #Para extraer e imprimir la primera hora
		# time0 = time[0];

		################################################################
		#Para almacenar todas las COTIZACIONES de codigo fuente
		price = re.findall(r'(\d{1},\d{3})',data);
		
		price_float=float(str(price[0]).replace(",", "."))

		#Para extraer e imprimir la primera hora
		price0 = price_float;
		
		urllib.urlopen("https://api.thingspeak.com/update?api_key=470WJU9MI5PGK4J1&field1="+str(price0))
		
		# db = MySQLdb.connect(host="localhost",user="phpmyadmin",passwd="hogar",db="bolsa_db")
		# # prepare a cursor object using cursor() method
		# cursor = db.cursor()
		# cursor.execute("INSERT INTO C (Precio,Tiempo,Fecha) VALUES (%s,%s,%s)",((price0),time0,date0))
		print price0
		return render_template('graph.html')
		
		


##############################################################################

if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0')







