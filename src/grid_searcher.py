import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from collections import defaultdict
import re

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import log_loss, mean_squared_error, r2_score, confusion_matrix
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import  RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
import xgboost as xgb
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction.text import HashingVectorizer, TfidfTransformer
from math import sqrt
import scipy.stats as stats
from scipy.stats import zscore

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical
from sklearn import preprocessing

print("loading data...")
_2019 = pd.read_csv('../data/IMDB_mine_data_2019.csv',index_col=0)
_2018 = pd.read_csv('../data/IMDB_mine_data_2018.csv',index_col=0)
_2017 = pd.read_csv('../data/IMDB_mine_data_2017.csv',index_col=0)
_2016 = pd.read_csv('../data/IMDB_mine_data_2016.csv',index_col=0)
_2015 = pd.read_csv('../data/IMDB_mine_data_2015.csv',index_col=0)
#get all the films into one DF
films = pd.concat([_2019,_2018,_2017,_2016,_2015])
# remove the filler films we were using to start the mining bot
films = films[films['title_code'] != np.nan]
films = films[films['opening_wknd'] != np.nan]
films = films[films['release_date'] != '1980-05-16']

print("filtering data...")
#clean the text in the production company column, and turn it into an accessable array
films['prod_co'] = films.prod_co.map(lambda x : re.findall(r"'(.*?)'",x, re.DOTALL))

#break production and distribution out into their own columns
films['production'] = films['prod_co'].map(lambda x : x[0] if len(x) >= 1 else np.nan)
films['production_2'] = films['prod_co'].map(lambda x : x[1] if len(x) >= 3 else np.nan)
films['distribution'] = films['prod_co'].map(lambda x : x[-1] if len(x) >= 2 else np.nan)

#convert the release date to a pandas datetime object
films['release_date'] = films['release_date'].map(lambda x : pd.to_datetime(x))

#Set the first director to their own column
films.directors = films.directors.map(lambda x : re.findall(r"'(.*?)'",x, re.DOTALL if isinstance(x, str) else np.nan))
films['director'] = films['directors'].map(lambda x: x[0].replace(" ", '') if len(x) >= 1 else 'none')

# convert the actor codes to strings
actor_key = pd.read_csv('../data/actor_key.csv', index_col=0).reset_index()

def get_actor_name(key):
    #print(key)
    if isinstance(key, float):
        return key
    row = actor_key.loc[actor_key['actor'] == key].index[0]
    #print(type(actor_key.iloc[row]['name']), actor_key.iloc[row]['name'])
    return actor_key.iloc[row]['name']

def get_actor_key(name):
    #print(key)
    row = actor_key.loc[actor_key['name'] == name].index[0]
    return(actor_key.iloc[row]['actor'])
print("generating features...")
films['actor_1'] = films['actor1'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_2'] = films['actor2'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_3'] = films['actor3'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_4'] = films['actor4'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_5'] = films['actor5'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_6'] = films['actor6'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_7'] = films['actor7'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_8'] = films['actor8'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_9'] = films['actor9'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)
films['actor_10'] = films['actor10'].map(lambda x : get_actor_name(x).replace(" ", '') if isinstance(x, str) else None)

print("generating more features...")
#Add the main producer and executive producer to the dataframe
producer_key = pd.read_csv('../data/producer_key.csv', index_col=0)
films = films.merge(producer_key, on='title_code', how='left')
#remove spaces in the names, and replace the fill values with empty strings
films['producer'] = films['producer'].map(lambda x : x.replace(" ", '') if x!='[]' else None)
films['executive'] = films['executive'].map(lambda x : x.replace(" ", '') if x!='[]' else None)

#reencode the release month as a string.
films['release_month'] = films['release_date'].map(lambda x : pd.to_datetime(x).month)
films['release_month'] = films['release_month'].map(lambda x : 'January' if x == 1 else ( 'February' if x==2 else ( 'March' if x==3 else ( 'April' if x==4 else ('May' if x==5 else ('June' if x==6 else ( 'July' if x==7 else ( 'August' if x==8 else ('September' if x==9 else ( 'October' if x==10 else ( 'November' if x==11 else ('December' if x==12 else 'unknown'))))))))) ) ))
#reencode the release year as a string
films['release_year'] = films['release_date'].map(lambda x : x.year)
films['release_year'] = films['release_year'].map(lambda x : '2015' if x == 2015 else ( '2016' if x==2016 else ( '2017' if x==2017 else ( '2018' if x==2018 else ('2019' if x==2019 else ('2020' if x==2020 else 'none'))))))

# Adding the genre OHE
# we need to extract the inner quotes from the strings into a list.
films['genre'] = films['genre'].map(lambda x : re.findall(r"'(.*?)'",x, re.DOTALL))
#we're going to do the OHE manually
films['action'] = films['genre'].map(lambda x : 1 if 'Action' in x else 0)
films['adventure']  = films['genre'].map(lambda x : 1 if 'Adventure' in x else 0)
films['animated'] = films['genre'].map(lambda x : 1 if 'Animation' in x else 0)
films['biography'] = films['genre'].map(lambda x : 1 if 'Biography' in x else 0)
films['drama'] = films['genre'].map(lambda x : 1 if 'Drama' in x else 0)
films['documentary'] = films['genre'].map(lambda x : 1 if 'Documentary' in x else 0)
films['comedy'] = films['genre'].map(lambda x : 1 if 'Comedy' in x else 0)
films['crime'] = films['genre'].map(lambda x : 1 if 'Crime' in x else 0)
films['fantasy'] = films['genre'].map(lambda x : 1 if 'Fantasy' in x else 0)
films['family'] = films['genre'].map(lambda x : 1 if 'Family' in x else 0)
films['musical'] = films['genre'].map(lambda x : 1 if 'Musical' in x else 0)
films['horror'] = films['genre'].map(lambda x : 1 if 'Horror' in x else 0)
films['war'] = films['genre'].map(lambda x : 1 if 'War' in x else 0)
films['mystery'] = films['genre'].map(lambda x : 1 if 'Mystery' in x else 0)
films['sci-fi'] = films['genre'].map(lambda x : 1 if 'Sci-Fi' in x else 0)
films['thriller'] = films['genre'].map(lambda x : 1 if 'Thriller' in x else 0)
films['romance'] = films['genre'].map(lambda x : 1 if 'Romance' in x else 0)

#add actor popularity scores
fake_popularity = 10071118 #instantiated as the lowest actor popularity +1
def get_act_pop(code, fake_pop):
    if code in act_pop_keys['actor'].unique():
        row = act_pop_keys.loc[act_pop_keys['actor'] == code].index[0]
        return act_pop_keys.iloc[row]['popularity']
    else:
        return fake_pop + randint(0,1000)

act_pop_keys = pd.read_csv('../data/actor_popularity.csv', index_col=0)
act_pop_keys.reset_index(inplace=True, drop=True)

films['actor1_popularity'] = films['actor1'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor2_popularity'] = films['actor2'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor3_popularity'] = films['actor3'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor4_popularity'] = films['actor4'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor5_popularity'] = films['actor5'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor6_popularity'] = films['actor6'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor7_popularity'] = films['actor7'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor8_popularity'] = films['actor8'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor9_popularity'] = films['actor9'].map(lambda x : get_act_pop(x,fake_popularity))
films['actor10_popularity'] = films['actor10'].map(lambda x : get_act_pop(x,fake_popularity))

print("still generating features...")
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

#convert popularity scores to text columns 
films['actor1_class'] = films['actor1_popularity'].map(lambda x : get_celeb_class(x))
films['actor2_class'] = films['actor2_popularity'].map(lambda x : get_celeb_class(x))
films['actor3_class'] = films['actor3_popularity'].map(lambda x : get_celeb_class(x))
films['actor4_class'] = films['actor4_popularity'].map(lambda x : get_celeb_class(x))
films['actor5_class'] = films['actor5_popularity'].map(lambda x : get_celeb_class(x))
films['actor6_class'] = films['actor6_popularity'].map(lambda x : get_celeb_class(x))
films['actor7_class'] = films['actor7_popularity'].map(lambda x : get_celeb_class(x))
films['actor8_class'] = films['actor8_popularity'].map(lambda x : get_celeb_class(x))
films['actor9_class'] = films['actor9_popularity'].map(lambda x : get_celeb_class(x))
films['actor10_class'] = films['actor10_popularity'].map(lambda x : get_celeb_class(x))

#create a vector from all the strings
films['train_string'] = films[['production','distribution','director','actor_1','actor_2','actor_3','actor_4',
                               'actor_5','actor_6','actor_7','actor_8','actor_9','actor_10',
                               'producer','executive']].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

print("Done generating features... filtering")
#add the normalized budget
bud = films[['budget']].values
min_max_scaler = preprocessing.MinMaxScaler()
bud_scaled = min_max_scaler.fit_transform(bud)
films['budget_normalized']=bud_scaled

#*******this block filters by zscore*********
# film_zscore = zscore(films.opening_wknd.to_numpy())
# abs_film_zscore = np.abs(film_zscore)
# filtered_entries = (abs_film_zscore < 3)
# filtered_df = films[filtered_entries].reset_index(drop=True)

#*******this filters by highest box office -ONLY-**********
#filtered_df = films[films.opening_wknd < films.opening_wknd.quantile(.97)].reset_index(drop=True)

#******this filters by largest and smallest box office to budget ratio, and highest outliers**********
films['pct_profit'] = films['opening_wknd'] / films['budget']
take = .98
filtered_df = films[films['opening_wknd'] < films['opening_wknd'].quantile(.97)].reset_index(drop=True)
filtered_df = filtered_df[filtered_df['pct_profit'] < filtered_df['pct_profit'].quantile(take)]
filtered_df = filtered_df[filtered_df['pct_profit'] > filtered_df['pct_profit'].quantile(1-take)].reset_index(drop=True)


#******this filters the films we suspect reported bad data**********
# filtered_df = filtered_df.drop(filtered_df[(filtered_df['budget'] != filtered_df['opening_wknd']) & 
#                                            (filtered_df['budget'] < 150000)].index).reset_index(drop=True)

# Make the vector from the strings
vectorizer = HashingVectorizer(n_features=1000)
vector = vectorizer.fit_transform(filtered_df['train_string'].to_numpy())
vec_df = pd.DataFrame.sparse.from_spmatrix(vector)

#make dummies from our curated columns
dum = pd.get_dummies(filtered_df[['release_month', 'actor1_class', 'actor2_class', 'actor3_class','rating']]) #'actor1_class', 'actor2_class', 'actor3_class',
dum.head(1)

#pull the columns we want from the main DF
use_cols = filtered_df[['budget','action','adventure','animated','biography','drama','documentary','comedy','crime',
                        'fantasy','family','musical','horror','war','mystery','sci-fi','thriller','romance']]

print("Splitting and training...")
#split for training
y = filtered_df['opening_wknd']
X = pd.concat([use_cols, dum, vec_df], axis=1, sort=False)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

model_g = GradientBoostingRegressor(learning_rate=0.02,
                                   n_estimators=200,
                                   min_samples_leaf=15,
                                   max_depth=400)
model_g.fit(X_train,y_train)
preds_gb = model_g.predict(X_test)
print("Trained model reports:")
print("MSE : " + str(mean_squared_error(y_test, preds_gb)))
print("RMSE: " + str(sqrt(mean_squared_error(y_test, preds_gb))))

#gradient boost searching
print("Beginning Gridsearch")
clf = GridSearchCV(model_g,
                   {'max_depth': [350,400,450],
                    'n_estimators': [350,400,450],
                   'min_samples_leaf':[12,15,17],
                   'learning_rate':[0.015,0.020,0.25]}, verbose=2, n_jobs=-1)
clf.fit(X, y)
print(clf.best_score_)
print(clf.best_params_)