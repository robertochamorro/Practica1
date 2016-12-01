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
	result_last = results[-1]
	

	db.commit()
	# disconnect from server
	cursor.close()
	db.close()
	
	#Poner URL de la empresa seleccionada para estudiar la cotizacion
	url = urllib.urlopen("http://www.infobolsa.es/cotizacion/grafico-b.popular")
	#Se almacena todo el codigo fuente de pagina "http://www.infobolsa.es/"
	data = url.read()

	#Para almacenar todas las COTIZACIONES de codigo fuente
	price = re.findall(r'(\d{1},\d{3})',data);
		
	price_float=float(str(price[0]).replace(",", "."))

	#Para extraer e imprimir la primera hora
	price0 = price_float;
	
	# collected_data_max = []
	# collected_data_min = []

	print last_result
	# for i in range(0, last_result):
		
	flag = 10
	if (price0 <= ((1-max) * (value_th)) ):#0.84
		flag = 0
		# collected_data_min.append(matrix[i]) # Your data
	elif (price0 >= ((1+max) * (value_th)) ):#0.86
		flag = 1
		# collected_data_max.append(matrix[i]) # Your data
		
	print value_th	
	print flag
	aux = 1	
	
	return render_template('index.html',flag = flag, max = max, result_last = result_last, aux = aux)
	
	# return jsonify(result_max=collected_data_max,result_min=collected_data_min)
	



	

###########################################################################	

@app.route('/average',methods=['POST'])

def average():
	db = MySQLdb.connect(host="localhost",user="phpmyadmin",passwd="hogar",db="bolsa_db")
	cursor = db.cursor()
	cursor.execute("SELECT AVG(Precio) FROM C")
	row = cursor.fetchone()	
	p_average = row[0]

	return render_template('average.html',p_average = p_average)
	
		
@app.route('/thingspeak',methods=['POST'])
def thingspeak():	
	while True:
		

		#Se debe realizar refresco en Thing Speak cada vez que se pulsa boton
		
		#Poner URL de la empresa seleccionada para estudiar la cotizacion
		url = urllib.urlopen("http://www.infobolsa.es/cotizacion/grafico-b.popular")
		#Se almacena todo el codigo fuente de pagina "http://www.infobolsa.es/"
		data = url.read()
		



		################################################################
		#Para almacenar todas las COTIZACIONES de codigo fuente
		price = re.findall(r'(\d{1},\d{3})',data);
		
		price_float=float(str(price[0]).replace(",", "."))

		#Para extraer e imprimir la primera hora
		price0 = price_float;
		
		urllib.urlopen("https://api.thingspeak.com/update?api_key=470WJU9MI5PGK4J1&field1="+str(price0))
		# aux=thingSpeakRead(196552,'ReadKey','31CKIR3Q4GICA0UB');
		
		# print aux
		print price0
		return render_template('graph.html')


		
		


##############################################################################

if __name__ == "__main__":
	app.debug = True
	app.run(host = '0.0.0.0')







