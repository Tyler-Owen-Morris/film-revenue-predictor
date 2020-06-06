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

# _2019 = pd.read_csv('../data/IMDB_mine_data_2019-oversample.csv',index_col=0)
# _2018 = pd.read_csv('../data/IMDB_mine_data_2018-oversample.csv',index_col=0)
# _2017 = pd.read_csv('../data/IMDB_mine_data_2017.csv',index_col=0)
# _2016 = pd.read_csv('../data/IMDB_mine_data_2016.csv',index_col=0)
# _2015 = pd.read_csv('../data/IMDB_mine_data_2015.csv',index_col=0)
# _2014 = pd.read_csv('../data/IMDB_mine_data_2014.csv',index_col=0)
# #get all the films into one DF
# films = pd.concat([_2019,_2018,_2017,_2016,_2015,_2014])
# title_string = '  |  '.join(films['title'].to_numpy())

all_titles = pd.read_csv('https://galvbucket.s3-us-west-1.amazonaws.com/titles_for_text_training.csv')
title_string = '  |  '.join(all_titles.title.to_numpy())

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
    print('''                                                       
@@@@@@@@  @@@@@@@    @@@@@@    @@@@@@@  @@@  @@@  @@@  
@@@@@@@@  @@@@@@@@  @@@@@@@@  @@@@@@@@  @@@  @@@  @@@  
@@!       @@!  @@@  @@!  @@@  !@@       @@!  @@@  @@!  
!@!       !@!  @!@  !@!  @!@  !@!       !@!  @!@  !@   
@!!!:!    @!@@!@!   @!@  !@!  !@!       @!@!@!@!  @!@  
!!!!!:    !!@!!!    !@!  !!!  !!!       !!!@!!!!  !!!  
!!:       !!:       !!:  !!!  :!!       !!:  !!!       
:!:       :!:       :!:  !:!  :!:       :!:  !:!  :!:  
:: ::::   ::       ::::: ::   ::: :::  ::   :::   ::  
: :: ::    :         : :  :    :: :: :   :   : :  :::  
                                                ''')
    print('----- Generating text after Epoch: %d' % epoch)

    if epoch >=10 and epoch % 3 == 0:
        start_index = random.randint(0, len(processed_text) - maxlen - 1)
        for temperature in [1.5]:
            print('----- temperature:', temperature)

            generated = ''
            sentence = processed_text[start_index: start_index + maxlen]
            generated += sentence
            print('----- Generating with seed: "' + sentence + '"')
            sys.stdout.write(generated)

            for i in range(2000):
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
            with open('../data/raw_generated_text.txt', "a+") as f:
                f.write(generated+"\n")
            print()
    else:
        pass
    pass


processed_text = title_string.lower()
processed_text = re.sub(r'[^\x00-\x7f]',r'', processed_text)
chars = sorted(list(set(processed_text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
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

# print('Load model...')
# model = keras.models.load_model('../data/title_generator2')

logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# Fit the model
print_callback = LambdaCallback(on_epoch_end=on_epoch_end)
print("fitting model")
model.fit(x, y,
        batch_size=128,
        epochs=151,
        callbacks=[print_callback])

#pickle.dump(model, open('../data/text_gen_model.pkl', "wb"))
print("***************")
print("MODEL FINISHED!")

model.save('../data/title_generator4')

#pickle.dump(nn_model, open('../data/text_gen_model.pkl', "wb"))
print("Script finished")