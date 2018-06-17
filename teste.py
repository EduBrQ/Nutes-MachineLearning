from flask import request, jsonify
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

from myapp import create_app
import pytest as pytest

app = Flask(__name__)
@app.route('/diabeteTeste')
def teste():
	with app.test_client() as c:
	    rv = c.post('/diabetes', json={
	        'Glucose': 999, 'BloodPressure': 999, 'Insulin': 100, 'BMI': 14, 'Age': 11
	    
	    })

	    return rv
	    
def test_answer1():
    assert teste() == 'Diabetes'

@app.route('/pressaoTeste')
def teste2():
	with app.test_client() as c:
	    rv = c.post('/pressao', json={
	        'Batimentos': 35, 'Calorias': 35
	    
	    })

	    return rv
def test_answer2():
    assert teste() == 'Sua Pressao esta normal'


############################################################

if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=33)