#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import nltk as nlp
import sys
import json

from sklearn.neural_network import MLPClassifier as Model
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
from nltk.corpus import stopwords


# In[ ]:

# In[2]:


def read_data():
    fake = pd.read_csv('./Datasets/fake-and-real-news-dataset/Fake.csv')
    real = pd.read_csv('./Datasets/fake-and-real-news-dataset/True.csv')
    fake['label'] = 0
    real['label'] = 1
    data = fake.append(real)
    data = data.sample(frac=0.05)
    return data


# In[3]:


def split_data(data):
    X = data[['text']]
    y = data['label']
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.3)
    return X_train, X_test, y_train, y_test


# In[4]:


def train_model():
    vectorizer = TfidfVectorizer(analyzer= 'word', lowercase= False, stop_words = nlp.corpus.stopwords.words('english'))
    data = read_data()
    #print(data)
    X_train, X_test, y_train, y_test = split_data(data)
    vectors = vectorizer.fit_transform(X_train.values.ravel())
    row, col = vectors.shape
    vectors = vectors.reshape(y_train.shape[0], int((row*col)/y_train.shape[0]))
    classifier = Model()
    classifier.fit(vectors, y_train.values.ravel())
    return (classifier, vectorizer)


# In[6]:


def predict(text):
    test = [[text]]
    df = pd.DataFrame(test, columns=["text"])
    (model, vectorizer) = train_model()
    df_vect = vectorizer.transform(df.values.ravel())
    row, col = df_vect.shape
    df_vect = df_vect.reshape(1, row * col)
    prediction = model.predict(df_vect)
    if prediction == 0:
        label = 'fake'
    else:
        label = 'real'
    return(label)


# In[8]:
text = sys.argv[1]
label = predict(text)
#print(label)
sys.stdout.write(label)

# In[ ]:









