# -*- coding: utf-8 -*-
"""LSTM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KC6kSql75ArLwt_ZAoF_Y9M3OEERS22j
"""

import re
import string
import numpy
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Masking
from keras.layers import Dense
from keras.layers import TimeDistributed

from google.colab import files
uploaded = files.upload()

with open('newMalData.txt') as f:
    arr = f.readlines()
    content = ''.join(arr)
    items = re.findall("^GET.*|POST.*$", content, re.MULTILINE)
    data = ""
    for item in items:
        temp_data = item.replace(" HTTP/1.1","").lower()
        data = data + temp_data + "\n"

chars = list(set(data + string.punctuation + string.ascii_lowercase + ' ' + string.digits))
VOCAB_SIZE = len(chars)
ix_to_char = {ix:char for ix, char in enumerate(chars)}
char_to_ix = {char:ix for ix, char in enumerate(chars)}
SEQ_LENGTH = 10
#print(chars)
DATA_LENGTH = int(len(data) / SEQ_LENGTH) 
#print(DATA_LENGTH, len(data))

X = numpy.zeros((DATA_LENGTH, SEQ_LENGTH, VOCAB_SIZE))
y = numpy.zeros((DATA_LENGTH, SEQ_LENGTH, VOCAB_SIZE))
for i in range(0, DATA_LENGTH):
    X_sequence = data[i*SEQ_LENGTH:(i+1)*SEQ_LENGTH]
    X_sequence_ix = [char_to_ix[value] for value in X_sequence]
    input_sequence = numpy.zeros((SEQ_LENGTH, VOCAB_SIZE))
    for j in range(SEQ_LENGTH):
        input_sequence[j][X_sequence_ix[j]] = 1.
    X[i] = input_sequence

    y_sequence = data[i*SEQ_LENGTH+1:(i+1)*SEQ_LENGTH+1]
    y_sequence_ix = [char_to_ix[value] for value in y_sequence]
    target_sequence = numpy.zeros((SEQ_LENGTH, VOCAB_SIZE))
    for j in range(SEQ_LENGTH):
        target_sequence[j][y_sequence_ix[j]] = 1.
    y[i] = target_sequence

model = Sequential()
model.add(LSTM(50, input_shape=(None, VOCAB_SIZE), return_sequences=True))
model.add(TimeDistributed(Dense(VOCAB_SIZE, activation='softmax')))
model.compile(loss='categorical_crossentropy', optimizer='adam')

model.fit(X, y, batch_size=4, verbose=1, nb_epoch=1)

model_json = model.to_json()
with open("LSTMmodel.json", "w") as json_file:
    json_file.write(model_json)
    
model.save_weights("LSTMmodel.h5")
print("Saved model to disk")

data=[]
with open('newMalTest.txt') as f:
    arr = f.readlines()
    content = ''.join(arr)
    items = re.findall("^GET.*|POST.*$", content, re.MULTILINE)
    for item in items:
        temp_data = item.replace(" HTTP/1.1","").lower()
        data.append(temp_data)
probability1=[]

ct=0
j=0
count=[0]*(len(data)+1)
print (len(count))
for seq in data:
    j+=1
    #print (seq)
    probability=[]
    X = numpy.zeros((1,len(seq),VOCAB_SIZE))
    for i in range(1,len(seq),1):
        ix = char_to_ix[seq[i-1]]
        X[0,i,:][ix]=1
    probability = model.predict_on_batch(X)
        #if (model.predict(X[:,:i,:])[0][0][char_to_ix[seq[i]]])<0.00001:
          #count[j]=1
          #print(j)
          #break
        #probability.append(model.predict(X[:,:i,:])[0][0][char_to_ix[seq[i]]])
        #X = numpy.zeros((1,len(seq),VOCAB_SIZE))
    #print(probability)
    for i in range(1,len(seq),1):
        if (probability[0][0][char_to_ix[seq[i]]]<0.00001):
            count[j]=1
            break

for i in count:
  ct+=i
print(ct,j)

print(float(ct)/float(j))
# 1142 1319

#ix = [numpy.random.randint(VOCAB_SIZE)]
#length = 100
#y_char = [ix_to_char[ix[-1]]]
#X = numpy.zeros((1,length,VOCAB_SIZE))
#for i in range(5):
#    X[0,i,:][ix[-1]]=1
#    print(model.predict(X[:,:i+1,:]))

