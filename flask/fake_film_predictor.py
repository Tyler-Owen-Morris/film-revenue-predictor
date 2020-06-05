import pandas as pd
import numpy as np
from random import randint
import re
import pickle
import random
from sklearn.feature_extraction.text import HashingVectorizer

#import the lists to make our random picks from.
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 
         'November', 'December']
genre = ['action','adventure','animated','biography','drama','documentary','comedy','crime','fantasy','family',
         'musical','horror','war','mystery','sci-fi','thriller','romance']
rating = ['G', 'PG', 'PG-13', 'R', 'not-rated']

actors = pd.read_csv('../data/all_actors.csv', index_col=0)
directors = pd.read_csv('../data/all_directors.csv', index_col=0)
production = pd.read_csv('../data/all_production.csv', index_col=0)
distribution = pd.read_csv('../data/all_distribution.csv', index_col=0)
producers = pd.read_csv('../data/all_producers.csv', index_col=0)
executives = pd.read_csv('../data/all_executives.csv', index_col=0)
budgets = pd.read_csv('../data/all_budgets.csv', index_col=0)
actor_key = pd.read_csv('../data/actor_key.csv', index_col=0).reset_index()
act_pop_keys = pd.read_csv('../data/actor_popularity.csv', index_col=0)
act_pop_keys.reset_index(inplace=True, drop=True)
model_gb = pickle.load(open('../data/gb_model.pkl', 'rb'))

def get_new_film_prediction():
    actor10 = actors['0'].sample(10).values
    director = directors.sample(1).values[0,0]
    prod = production.sample(1).values[0,0]
    dist = distribution.sample(1).values[0,0]
    producer = producers.sample(1).values[0,0]
    executive = executives.sample(1).values[0,0]
    budget = budgets.sample(1).values[0,0]

    film = pd.DataFrame(columns=['actor1', 'actor2', 'actor3', 'actor4', 'actor5', 'actor6', 'actor7', 'actor8', 'actor9',
                                'actor10', 'director', 'production', 'distribution', 'producer', 'executive', 'budget'])
    film.loc[0] = [actor10[0], actor10[1], actor10[2], actor10[3], actor10[4], actor10[5], actor10[6]
                , actor10[7], actor10[8], actor10[9], director, prod, dist, producer, executive, budget]
    
    rate = random.choice(rating)
    genres = random.sample(genre,3)
    month = random.choice(months)
    print("you are making a "+ str(rate)+" rated film of the "+ ', '.join([str(x) for x in genres]) +" sort of genre, that comes out in "+str(month))

    film['rating'] = rate
    film['genre'] = [genres]
    film['release_month'] = month

    film['actor_1'] = film['actor1'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_2'] = film['actor2'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_3'] = film['actor3'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_4'] = film['actor4'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_5'] = film['actor5'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_6'] = film['actor6'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_7'] = film['actor7'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_8'] = film['actor8'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_9'] = film['actor9'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
    film['actor_10'] = film['actor10'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)

    film['actor_1_string'] = film['actor1'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_2_string'] = film['actor2'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_3_string'] = film['actor3'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_4_string'] = film['actor4'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_5_string'] = film['actor5'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_6_string'] = film['actor6'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_7_string'] = film['actor7'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_8_string'] = film['actor8'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_9_string'] = film['actor9'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)
    film['actor_10_string'] = film['actor10'].map(lambda x : get_actor_name(x) if isinstance(x, str) else None)

    film['train_string'] = film[['production','distribution','director','actor_1','actor_2','actor_3','actor_4',
                               'actor_5','actor_6','actor_7','actor_8','actor_9','actor_10',
                               'producer','executive']].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

    #we're going to do the OHE manually
    film['action'] = film['genre'].map(lambda x : 1 if 'Action' in x else 0)
    film['adventure']  = film['genre'].map(lambda x : 1 if 'Adventure' in x else 0)
    film['animated'] = film['genre'].map(lambda x : 1 if 'Animation' in x else 0)
    film['biography'] = film['genre'].map(lambda x : 1 if 'Biography' in x else 0)
    film['drama'] = film['genre'].map(lambda x : 1 if 'Drama' in x else 0)
    film['documentary'] = film['genre'].map(lambda x : 1 if 'Documentary' in x else 0)
    film['comedy'] = film['genre'].map(lambda x : 1 if 'Comedy' in x else 0)
    film['crime'] = film['genre'].map(lambda x : 1 if 'Crime' in x else 0)
    film['fantasy'] = film['genre'].map(lambda x : 1 if 'Fantasy' in x else 0)
    film['family'] = film['genre'].map(lambda x : 1 if 'Family' in x else 0)
    film['musical'] = film['genre'].map(lambda x : 1 if 'Musical' in x else 0)
    film['horror'] = film['genre'].map(lambda x : 1 if 'Horror' in x else 0)
    film['war'] = film['genre'].map(lambda x : 1 if 'War' in x else 0)
    film['mystery'] = film['genre'].map(lambda x : 1 if 'Mystery' in x else 0)
    film['sci-fi'] = film['genre'].map(lambda x : 1 if 'Sci-Fi' in x else 0)
    film['thriller'] = film['genre'].map(lambda x : 1 if 'Thriller' in x else 0)
    film['romance'] = film['genre'].map(lambda x : 1 if 'Romance' in x else 0)

    fake_popularity = 10071118
    film['actor1_popularity'] = film['actor1'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor2_popularity'] = film['actor2'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor3_popularity'] = film['actor3'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor4_popularity'] = film['actor4'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor5_popularity'] = film['actor5'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor6_popularity'] = film['actor6'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor7_popularity'] = film['actor7'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor8_popularity'] = film['actor8'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor9_popularity'] = film['actor9'].map(lambda x : get_act_pop(x,fake_popularity))
    film['actor10_popularity'] = film['actor10'].map(lambda x : get_act_pop(x,fake_popularity))

    #convert popularity scores to text columns 
    film['actor1_class'] = film['actor1_popularity'].map(lambda x : get_celeb_class(x))
    film['actor2_class'] = film['actor2_popularity'].map(lambda x : get_celeb_class(x))
    film['actor3_class'] = film['actor3_popularity'].map(lambda x : get_celeb_class(x))
    film['actor4_class'] = film['actor4_popularity'].map(lambda x : get_celeb_class(x))
    film['actor5_class'] = film['actor5_popularity'].map(lambda x : get_celeb_class(x))
    film['actor6_class'] = film['actor6_popularity'].map(lambda x : get_celeb_class(x))
    film['actor7_class'] = film['actor7_popularity'].map(lambda x : get_celeb_class(x))
    film['actor8_class'] = film['actor8_popularity'].map(lambda x : get_celeb_class(x))
    film['actor9_class'] = film['actor9_popularity'].map(lambda x : get_celeb_class(x))
    film['actor10_class'] = film['actor10_popularity'].map(lambda x : get_celeb_class(x))

    #reload the variable
    dummy_blank = pd.read_csv('../data/dummy_blank.csv', index_col=0)
    dummy_blank.iloc[0, dummy_blank.columns.get_loc('release_month_'+film['release_month'][0]) ] = 1
    dummy_blank.iloc[0, dummy_blank.columns.get_loc('actor1_class_'+film['actor1_class'][0]) ] = 1
    dummy_blank.iloc[0, dummy_blank.columns.get_loc('actor2_class_'+film['actor2_class'][0]) ] = 1
    dummy_blank.iloc[0, dummy_blank.columns.get_loc('actor3_class_'+film['actor3_class'][0]) ] = 1
    if film['rating'][0] == 'not-rated':
        dummy_blank.iloc[0, dummy_blank.columns.get_loc('rating_'+'Not Rated') ] = 1
    else:
        dummy_blank.iloc[0, dummy_blank.columns.get_loc('rating_'+film['rating'][0]) ] = 1

    vectorizer = HashingVectorizer(n_features=1000)
    vector = vectorizer.fit_transform(film['train_string'].to_numpy())
    vec_df = pd.DataFrame.sparse.from_spmatrix(vector)
    use_cols = film[['budget','action','adventure','animated','biography','drama','documentary','comedy','crime',
                        'fantasy','family','musical','horror','war','mystery','sci-fi','thriller','romance']]
    X = pd.concat([use_cols, dummy_blank, vec_df], axis=1, sort=False)

    prediction = model_gb.predict(X)
    
    #construct return dict with prediction
    r = {}
    r['predicted_revenue'] = round(prediction[0],2)
    r['director'] = director
    r['producer'] = producer
    r['executive'] = executive
    r['release_month'] = month
    r['budget'] = budget
    r['actor1'] = film.actor_1_string[0]
    r['actor2'] = film.actor_2_string[0]
    r['actor3'] = film.actor_3_string[0]
    r['actor4'] = film.actor_4_string[0]
    r['actor5'] = film.actor_5_string[0]
    r['actor6'] = film.actor_6_string[0]
    r['actor7'] = film.actor_7_string[0]
    r['actor8'] = film.actor_8_string[0]
    r['actor9'] = film.actor_9_string[0]
    r['actor10'] = film.actor_10_string[0]
    r['production'] = film.production[0]
    r['distribution'] = film.distribution[0]
    r['genre'] = film.genre[0]
    return r

def get_celeb_class(pop):
    if pop <=2000:
        return 'A-list'
    elif pop <= 5000:
        return 'B-list'
    elif pop <= 20000:
        return 'C-list'
    elif pop <= 100000:
        return 'D-list'
    elif pop <= 250000:
        return 'E-list'
    else:
        return 'nobody'

def get_act_pop(code, fake_pop):
    if code in act_pop_keys['actor'].unique():
        row = act_pop_keys.loc[act_pop_keys['actor'] == code].index[0]
        return act_pop_keys.iloc[row]['popularity']
    else:
        return fake_pop + randint(0,1000)
    
def get_actor_name(key):
    #print(key)
    if isinstance(key, float):
        return key
    row = actor_key.loc[actor_key['actor'] == key].index[0]
    #print(type(actor_key.iloc[row]['name']), actor_key.iloc[row]['name'])
    return actor_key.iloc[row]['name']