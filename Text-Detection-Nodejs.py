#!/usr/bin/env python
# coding: utf-8

# In[1]:


from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import cv2
import os
import pytesseract
import urllib.request
import requests
import sys


# In[ ]:


pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'


# In[2]:


args = {"east":"/home/janhavi/Documents/chatbot/Datasets/frozen_east_text_detection.pb", "min_confidence":0.1, "width":320, "height":320}


# In[3]:


def resize(filename):
    image = cv2.imread(filename, cv2.IMREAD_COLOR)
    orig = image.copy()
    (origH, origW) = image.shape[:2]
    (newW, newH) = (args['width'], args['height'])
    rW = origW / float(newW)
    rH = origH / float(newH)
    image = cv2.resize(image, (newW, newH))
    (H, W) = image.shape[:2]
    return orig, image, H, W, rH, rW


# In[4]:


def EAST(image):
    blob = cv2.dnn.blobFromImage(image, 1.0, (W, H), (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net = cv2.dnn.readNet("/app/frozen_east_text_detection.pb")
    layerNames = ["feature_fusion/Conv_7/Sigmoid","feature_fusion/concat_3"]
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)
    return (scores, geometry)    


# In[5]:


def predictions(prob_score, geo):
    (numR, numC) = prob_score.shape[2:4]
    boxes = []
    confidence_val = []
    count = 0
    
    for y in range(0,numR):
        scoresData = prob_score[0,0,y]
        x0 = geo[0, 0, y]
        x1 = geo[0, 1, y]
        x2 = geo[0, 2, y]
        x3 = geo[0, 3, y]
        anglesData = geo[0, 4, y]
        
        for i in range(0,numC):
            if scoresData[i] < 0.5:
                continue

            (offX, offY) = (i * 4.0, y * 4.0)

            angle = anglesData[i]
            cos = np.cos(angle)
            sin = np.sin(angle)

            h = x0[i] + x2[i]
            w = x1[i] + x3[i]

            endX = int(offX + (cos * x1[i]) + (sin * x2[i]))
            endY = int(offY - (sin * x1[i]) + (cos * x2[i]))
            startX = int(endX - w)
            startY = int(endY - h)

            boxes.append((startX, startY, endX, endY))
            confidence_val.append(scoresData[i])
    
    return (boxes, confidence_val)


# In[6]:


def predict_text(orig, image, rH, rW):
    scores, geometry = EAST(image)
    boxes, confidence_val = predictions(scores, geometry)
    boxes = non_max_suppression(np.array(boxes), probs = confidence_val)
    results = []
    words = []
    for (startX, startY, endX, endY) in boxes:
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        r = orig[startY:endY, startX:endX]  
        gray = cv2.cvtColor(r, cv2.COLOR_BGR2GRAY)
        (thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(blackAndWhiteImage, config = "-l eng --oem 1 --psm 8")
        words.append(text)
    return words


# In[7]:


url = sys.argv[1]
filename = 'detect_img.png'
THIS_FOLDER = os.path.dirname(os.path.abspath(filename))
with open('{}/{}'.format(THIS_FOLDER, filename),'wb') as f:
    image_url = url
    f.write(requests.get(image_url).content)
orig, image, H, W, rH, rW = resize(filename)
predict = predict_text(orig, image, rH, rW)
os.remove(filename)
word = ""
for i in predict:
    word = word + ' ' + i
sys.stdout.write(word)

# In[ ]:





# In[ ]:




