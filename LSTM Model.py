#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import tensorflow
from keras.models import model_from_json
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
import sys


# In[ ]:


json_file = open('model.json','r')


# In[ ]:


model_json = json_file.read()
json_file.close()


# In[ ]:


model = model_from_json(model_json)


# In[ ]:


model.load_weights("model.h5")


# In[ ]:


model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])


# In[ ]:


#hyperparameters
EMBEDDING_DIMENSION = 64
VOCABULARY_SIZE = 1000
MAX_LENGTH = 200
OOV_TOK = '<OOV>'
TRUNCATE_TYPE = 'post'
PADDING_TYPE = 'post'


# In[ ]:


import pickle
tokenizer = pickle.load(open("tokenizer.pickle", 'rb'))


# In[ ]:


text = sys.argv[1]
text = [text]


# In[ ]:


text = text.str.lower()


# In[ ]:


def remove_stop_words(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [w for w in tokens if not w in stop_words]  
    return ''.join(filtered_tokens)
text = list(map(remove_stop_words, text))


# In[ ]:


#Lemmatize text
def getLemm(text):
    tokens = word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return ''.join(tokens)

text = list(map(getLemm, text))


# In[ ]:


sequence = tokenizer.texts_to_sequences(text)
padded_sequence = sequence.pad_sequences(sequence, maxlen = MAX_LENGTH, padding = PADDING_TYPE, truncating = TRUNCATE_TYPE)


# In[ ]:


prediction = model.predict_classes(padded_sequence)
labels = ['Fake', 'Real', 'Mixture', 'Miscaptioned', 'Verified Scam']
sys.stdout.write(labels(prediction[0]))

