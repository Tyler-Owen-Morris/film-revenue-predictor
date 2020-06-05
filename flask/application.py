from flask import Flask, render_template, request, redirect, url_for
import pickle
import json
app = Flask(__name__)
import psycopg2
import time
from fake_film_predictor import get_new_film_prediction

@app.route("/", methods=['POST','GET'])
def home():
    return render_template('home.html')

@app.route("/details", methods=['POST','GET'])
def details():
    data = get_new_film_prediction()
    print("loaded into details page")
    return render_template('details.html', data=data)

if __name__=='__main__':
    app.run(debug=True)
    


