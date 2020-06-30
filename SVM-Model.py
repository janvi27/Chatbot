#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pickle
from sklearn.feature_extraction.text import CountVectorizer
import sys


# In[5]:


model = pickle.load(open("SVM.sav", 'rb'))
vocab = pickle.load(open("vocabulary.pk1", 'rb'))


# In[6]:


text = sys.argv[1]


# In[8]:


text = [text]


# In[9]:


vector = CountVectorizer(decode_error = "replace", vocabulary = vocab)
vectorized_text = vector.transform(text)


# In[11]:


prediction = model.predict(vectorized_text)
labels = ['Fake', 'Real', 'Mixture', 'Miscaptioned', 'Verified Scam']
sys.stdout.write(labels(prediction[0]))


# In[ ]:





# In[ ]:




