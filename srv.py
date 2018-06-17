import numpy as np
from flask import Flask, abort, jsonify, request
import pickle as pickle

import numpy as np
import base64

from flask import Flask, request, render_template, make_response
from sklearn.externals import joblib
from io import BytesIO
from skimage import io as skio
from skimage.transform import resize
from flask import Flask, render_template
import requests
import json
import sys
##############################################
###-CARREGO MEU MODELO DE APRENDIZAGEM AQUI-##
##############################################
my_knn = pickle.load(open('analytics_folder/knn.pkl', 'rb'))

diabetes_model = pickle.load(open('analytics_folder/diabetes.pkl', 'rb')) 
app = Flask(__name__)

##############################################
################ -API HOME - #################
##############################################
@app.route('/home')

def home():
    return ("Página Ínicial")

###############################################
############## -ROTA SWAGGER - ################
###############################################


    
###############################################
# ROTA (POST) QUE RECEBE OS ATRIBUTOS ESPERADOS DO MODELO DE APRENDIZAGEM DEFINIDO E RETORNA A PREDIÇÃO FEITA POR ELE
@app.route('/pressao', methods=['POST'])

def make_predict(): #10.0.0.102
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            predict_request = [data['Batimentos'], data['Calorias']]
            
        except ValueError:
            return jsonify("Por favor, coloque um valor para batimentos e calorias: ")
        
    predict_request = np.array(predict_request)
    predict_request = predict_request.reshape(1,-1)

    y_hat = my_knn.predict(predict_request) #retorna o resulta em JSON

    output = [y_hat[0]]
    
    #return jsonify(my_knn.predict(predict_request).tolist()) #Transforma o resultado JSON em uma lista
                   
    def result(m):
        if m[0] == 0:
            return "Sua Pressao esta normal"
        
        elif m[0] == 1:
            return "Sua Pressao esta muito Baixa"
        
        elif m[0] == 2:
            return "Sua Pressao esta muito Alta"
   
    output = result(output)
    return jsonify(results=output)
###############################################


# ROTA (POST) QUE RECEBE OS ATRIBUTOS ESPERADOS DO MODELO DE APRENDIZAGEM DEFINIDO E RETORNA A PREDIÇÃO FEITA POR ELE
@app.route('/diabetes', methods=['POST'])

def make_predict2(): #10.0.0.102
    if request.method == 'POST':
        try:
            data = request.get_json(force=True)
            #predict_request = [data['Pregnancies'], data['Glucose'], data['BloodPressure'], data['SkinThickness'], data['Insulin'], data['BMI'], data['DiabetesPedigreeFunction'], data['Age']]
            predict_request = [data['Glucose'], data['BloodPressure'], data['Insulin'], data['BMI'], data['Age']]
            
        except ValueError:
            return jsonify("Valores inadequados! ")
        
    predict_request = np.array(predict_request)
    predict_request = predict_request.reshape(1,-1)

    y_hat2 = diabetes_model.predict(predict_request) #retorna o resulta em JSON

    output2 = [y_hat2[0]]
    
    #return jsonify(my_knn.predict(predict_request).tolist()) #Transforma o resultado JSON em uma lista
                   
    def result(m):
        if m[0] == 0:
            return "Sem Diabetes"
        
        elif m[0] == 1:
            return "Diabetes"
      
   
    output2 = result(output2)
    return jsonify(results=output2)
###############################################


# A route to return all of the available entries in our catalog.
@app.route('/hanUser', methods=['GET'])
def api_all():
	params = {
    'api_key': '{eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1YWNjYjZkYTM3MzNjZDAwMTQ5MTZjNTAifQ.1gJH3Y0u9vmXcYQsMx-OmqqFL2rQfTZlYF9L4r9bXO0}',
  }
	r = requests.get('https://haniot-api.herokuapp.com/api/v1/measurements/types/3?period=3w', headers={'Authorization': 'JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfaWQiOiI1YWNjYjZkYTM3MzNjZDAwMTQ5MTZjNTAifQ.1gJH3Y0u9vmXcYQsMx-OmqqFL2rQfTZlYF9L4r9bXO0'})
	#r = get_json(r.text)
	r = r.text

	return r

###############################################
################# -TESTES- ####################
###############################################
@app.route('/diabeteTeste')
def teste():
	with app.test_client() as c:
	    rv = c.post('/diabetes', json={
	        'Glucose': 999, 'BloodPressure': 999, 'Insulin': 100, 'BMI': 14, 'Age': 11
	    
	    })
	    print(rv, file=sys.stderr)
	    return rv

@app.route('/pressaoTeste')
def teste2():
	with app.test_client() as c:
	    rv = c.post('/pressao', json={
	        'Batimentos': 35, 'Calorias': 35
	    
	    })
	    print(rv, file=sys.stderr)
	    return rv

@app.route('/aquisicaoTeste')
def teste3():
	with app.test_client() as c:
	    resp = c.get('/hanUser')
	    print(resp, file=sys.stderr)
	    return resp
############################################################

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=33)