import pandas as pd
import numpy as np
import logging, os
import re
import boto3
import sys
import pickle
import random
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.callbacks import LambdaCallback

_2019 = pd.read_csv('../data/IMDB_mine_data_2019-oversample.csv',index_col=0)
_2018 = pd.read_csv('../data/IMDB_mine_data_2018-oversample.csv',index_col=0)
_2017 = pd.read_csv('../data/IMDB_mine_data_2017.csv',index_col=0)
_2016 = pd.read_csv('../data/IMDB_mine_data_2016.csv',index_col=0)
_2015 = pd.read_csv('../data/IMDB_mine_data_2015.csv',index_col=0)
_2014 = pd.read_csv('../data/IMDB_mine_data_2014.csv',index_col=0)
#get all the films into one DF
films = pd.concat([_2019,_2018,_2017,_2016,_2015,_2014])
title_string = ' '.join(films['title'].to_numpy())

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)

def on_epoch_end(epoch, _):
    # Function invoked at end of each epoch. Prints generated text.
    print("****************************************************************************")
    print('----- Generating text after Epoch: %d' % epoch)

    print("we're not generating text with this")
    pass

def make_model(string):
    processed_text = string.lower()
    processed_text = re.sub(r'[^\x00-\x7f]',r'', processed_text)
    chars = sorted(list(set(processed_text)))
    print('total chars:', len(chars))
    char_indices = dict((c, i) for i, c in enumerate(chars))
    indices_char = dict((i, c) for i, c in enumerate(chars))

    # cut the text in semi-redundant sequences of maxlen characters
    maxlen = 20
    step = 3
    sentences = []
    next_chars = []
    for i in range(0, len(processed_text) - maxlen, step):
        sentences.append(processed_text[i: i + maxlen])
        next_chars.append(processed_text[i + maxlen])

    x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
    y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
    for i, sentence in enumerate(sentences):
        for t, char in enumerate(sentence):
            x[i, t, char_indices[char]] = 1
        y[i, char_indices[next_chars[i]]] = 1

    print('Build model...')
    model = Sequential()
    model.add(LSTM(128, input_shape=(maxlen, len(chars))))
    model.add(Dense(len(chars), activation='softmax'))

    optimizer = RMSprop(lr=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    logging.disable(logging.WARNING)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

    # Fit the model
    print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
    print("fitting model")
    model.fit(x, y,
            batch_size=128,
            epochs=10,
            callbacks=[print_callback])

    #pickle.dump(model, open('../data/text_gen_model.pkl', "wb"))
    print("***************")
    print("MODEL FINISHED!")
    return model

nn_model = make_model(title_string)

bucket='galvbucket'
key='titlemaker_trained_model.pkl'
pickle_byte_obj = pickle.dumps(nn_model) 
s3_resource = boto3.resource('s3')
s3_resource.Object(bucket,key).put(Body=pickle_byte_obj)

#pickle.dump(nn_model, open('../data/text_gen_model.pkl', "wb"))
print("Script finished")