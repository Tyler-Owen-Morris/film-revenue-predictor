from flask import Flask, Response, render_template, request, redirect, url_for
import pickle
import json
import pandas as pd
from wtforms import TextField, Form, SubmitField
application = app = Flask(__name__)
import time
from fake_film_predictor import get_new_film_prediction
from fake_film_predictor import get_gold_film_prediction

actors = pd.read_csv('../data/actor_key.csv', index_col=0).name.values.tolist()
directors = pd.read_csv('../data/all_directors.csv', index_col=0)['0'].values.tolist()

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
    if request.method == 'POST':
        first_actor = str(request.form['input1'])
        second_actor = str(request.form['input2'])
        third_actor = str(request.form['input3'])
        fourth_actor = str(request.form['input4'])
        fifth_actor = str(request.form['input5'])
        director = str(request.form.get('inputD'))
        genres = request.form.getlist('genreCheckbox')
        actor = [first_actor, second_actor, third_actor, fourth_actor, fifth_actor]
        rating = request.form.get('ratingCheckbox')
        print(director)
        print(actor)
        print(genres)
        print(rating)
        
    return render_template('custom.html', form=form)

#auto complete feature for actors
@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    #print("Autocomplete called!")
    #print(len(actors))
    return Response(json.dumps(actors), mimetype='application/json')

@app.route('/_autocompleteD', methods=['GET'])
def autocompleteD():
    print("AutocompleteD called!")
    print(len(directors))
    return Response(json.dumps(directors), mimetype='application/json')

if __name__=='__main__':
    app.run(debug=True)