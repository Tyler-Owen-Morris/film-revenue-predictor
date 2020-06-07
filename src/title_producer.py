import numpy as np
import pandas as pd
import random
import re
import logging, os
import sys
from tensorflow import keras

_2019 = pd.read_csv('../data/IMDB_mine_data_2019-oversample.csv',index_col=0)
_2018 = pd.read_csv('../data/IMDB_mine_data_2018-oversample.csv',index_col=0)
_2017 = pd.read_csv('../data/IMDB_mine_data_2017.csv',index_col=0)
_2016 = pd.read_csv('../data/IMDB_mine_data_2016.csv',index_col=0)
_2015 = pd.read_csv('../data/IMDB_mine_data_2015.csv',index_col=0)
_2014 = pd.read_csv('../data/IMDB_mine_data_2014.csv',index_col=0)
#get all the films into one DF
films = pd.concat([_2019,_2018,_2017,_2016,_2015,_2014])
title_string = '  |  '.join(films['title'].to_numpy())

# all_titles = pd.read_csv('https://galvbucket.s3-us-west-1.amazonaws.com/titles_for_text_training-unique.csv')
# title_string = '  |  '.join(all_titles.title.to_numpy())

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def spit_out_text():
    # Function invoked at end of each epoch. Prints generated text.
    print("****************************************************************************")
    #print('----- Generating text after Epoch: %d' % epoch)
    
    start_index = random.randint(0, len(processed_text) - maxlen - 1)
    for temperature in [1.0]:
        print('----- temperature:', temperature)

        generated = ''
        sentence = processed_text[start_index: start_index + maxlen]
        #sentence = 'the matrix  |  the fifth element  |  han'
        generated += sentence
        print('----- Generating with seed: "' + sentence + '"')
        sys.stdout.write(generated)

        for i in range(1000):
            x_pred = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x_pred[0, t, char_indices[char]] = 1.

            preds = model.predict(x_pred, verbose=0)[0]
            next_index = sample(preds, temperature)
            next_char = indices_char[next_index]

            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()
        with open('../data/raw_generated_text_aws.txt', "a+") as f:
              f.write(generated[maxlen:]+"\n")
        print()

# ***************** EVERYTHING BELOW HERE RUNS AFTER ALL FUNCTIONS AND DATA HAVE BEEN LOADED ****************

processed_text = title_string.lower()
processed_text = re.sub(r'[^\x00-\x7f]',r'', processed_text)
chars = sorted(list(set(processed_text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3

print('Load model...')
model = keras.models.load_model('../data/title_generator_working')

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

for _ in range(20):
    spit_out_text()

print("Script finished")