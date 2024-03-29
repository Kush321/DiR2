import cv2
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.datasets import fetch_openml
from PIL import Image
import PIL.ImageOps
import os,ssl,time
x, y = fetch_openml('mnist_784', version=1, return_X_y=True)
b = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
n = len(b)
xt, xtt, yt, ytt = train_test_split(x, y, test_size=2500, random_state=0, train_size=7500)
k = xt/255
o = xtt/255
clf = LogisticRegression(solver='saga', multi_class='multinomial').fit(k, yt)
prediction = clf.predict(o)
accuracy = accuracy_score(ytt, prediction)
print(accuracy)

#for camera
g = cv2.VideoCapture(0)
while(True): 
    try: 
        ret, frame = g.read() 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        height, width = gray.shape
        upper_left = (int(width / 2 - 56), int(height / 2 - 56)) 
        bottom_right = (int(width / 2 + 56), int(height / 2 + 56)) 
        cv2.rectangle(gray, upper_left, bottom_right, (0, 255, 0), 2)

        roi = gray[upper_left[1]:bottom_right[1], upper_left[0]:bottom_right[0]] 
        
        im_pil = Image.fromarray(roi) 
        image_bw = im_pil.convert('L') 
        image_bw_resized = image_bw.resize((28,28), Image.ANTIALIAS) 
        image_bw_resized_inverted = PIL.ImageOps.invert(image_bw_resized) 
        pixel_filter = 20 
        min_pixel = np.percentile(image_bw_resized_inverted, pixel_filter) 
        image_bw_resized_inverted_scaled = np.clip(image_bw_resized_inverted-min_pixel, 0, 255) 
        max_pixel = np.max(image_bw_resized_inverted) 
        image_bw_resized_inverted_scaled = np.asarray(image_bw_resized_inverted_scaled)/max_pixel 
        test_sample = np.array(image_bw_resized_inverted_scaled).reshape(1,784) 
        test_pred = clf.predict(test_sample) 
        print("Predicted class is: ", test_pred)
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    except Exception as e:
        pass
g.release()
cv2.destroyAllWindows()