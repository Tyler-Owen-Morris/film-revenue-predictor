from flask import Flask, Response, render_template, request, redirect, url_for
import pickle
import json
import pandas as pd
from wtforms import TextField, Form, SubmitField
application = app = Flask(__name__)
import time
from fake_film_predictor import get_new_film_prediction
from fake_film_predictor import get_gold_film_prediction, get_custom_film_prediciton

actors = pd.read_csv('https://galvbucket.s3-us-west-1.amazonaws.com/flask_data/actor_key.csv', index_col=0).name.values.tolist()
directors = pd.read_csv('https://galvbucket.s3-us-west-1.amazonaws.com/flask_data/all_directors.csv', index_col=0)['0'].values.tolist()

class SearchForm(Form):
    autocomp = TextField('Actor name', id='actor_autocomplete')

@app.route("/", methods=['POST','GET'])
def home():
    return render_template('home.html')

@app.route("/details", methods=['POST','GET'])
def details():
    gold = str(request.args.get('type'))
    if gold == 'golden':
        data = get_gold_film_prediction()
    else:
        data = get_new_film_prediction()
    print("loaded into details page")
    return render_template('details.html', data=data)

@app.route("/custom", methods=['POST','GET'])
def custom():
    #print(actors)
    form = SearchForm(request.form)
    budgets = [10000,100000,1000000,100000000,200000000]
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 
         'November', 'December']
    if request.method == 'POST':
        first_actor = str(request.form['input1'])
        second_actor = str(request.form['input2'])
        third_actor = str(request.form['input3'])
        fourth_actor = str(request.form['input4'])
        fifth_actor = str(request.form['input5'])
        sixth_actor = str(request.form['input6'])
        seventh_actor = str(request.form['input7'])
        eighth_actor = str(request.form['input8'])
        ninth_actor = str(request.form['input9'])
        tenth_actor = str(request.form['input10'])
        director = str(request.form.get('inputD'))
        genres = request.form.getlist('genreCheckbox')
        actors = [first_actor, second_actor, third_actor, fourth_actor, fifth_actor, sixth_actor, seventh_actor, eighth_actor, ninth_actor, tenth_actor]
        rating = request.form.get('ratingCheckbox')
        budget = request.form.get('budget')
        prod = request.form.get('production')
        dist = request.form.get('distribution')
        month = request.form.get('month')
        # print(director)
        # print(actor)
        print(genres)
        print(rating)
        # print(budget)
        # print(prod,dist)
        data = get_custom_film_prediciton(director, actors, genres, rating, budget, prod, dist, month)
        return render_template('details.html', data=data)
    
    productions = pd.read_csv('https://galvbucket.s3-us-west-1.amazonaws.com/flask_data/all_production.csv', index_col=0)['0'].values.tolist()
    distributors = pd.read_csv('https://galvbucket.s3-us-west-1.amazonaws.com/flask_data/all_distribution.csv', index_col=0)['0'].values.tolist()[1:]
    return render_template('custom.html', form=form, months=months, budgets=budgets, productions=productions, distributors=distributors)

#auto complete feature for actors
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    #print("Autocomplete called!")
    #print(len(actors))
    return Response(json.dumps(actors), mimetype='application/json')

@app.route('/_autocompleteD', methods=['GET'])
def autocompleteD():
    #print("AutocompleteD called!")
    #print(len(directors))
    return Response(json.dumps(directors), mimetype='application/json')

if __name__=='__main__':
    app.run(host='0.0.0.0', port=80, debug=True)