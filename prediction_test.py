# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 17:59:36 2022
# @author: alexhou00
"""
from keras.models import load_model
import cv2
import numpy as np

model = load_model('Xception_model_20220710_9761.h5')
test_image = cv2.imread(r"C:\Users\alexh\Pictures\LoGaRT\1.jpg")
image_file_resize = cv2.resize(test_image, (128, 128), interpolation=cv2.INTER_AREA)
test_pred = model.predict(np.array([image_file_resize]), verbose=1)
test_pred_p = test_pred * 100
test_pred_p = test_pred_p.astype('int32')
test_pred_p_sorted = np.sort(test_pred_p)
test_pred_p_sorted = test_pred_p_sorted[:, ::-1]
test_pred_p_arg = np.argsort(test_pred_p)
test_pred_p_arg = test_pred_p_arg[:, ::-1]
test_pred = np.argmax(test_pred, axis=1)
# string = ""
# test_label_1 = np.argmax(test_label, axis=1)

display_labels = ['0 text', '1 scenic', '2 city', '3 admin', '4 star',
                  '5 photo', '6 human', '7 object', '8 bldg', '9 ritual']
for i, j in zip(test_pred_p_arg[0], test_pred_p_sorted[0]):
    print(display_labels[i].ljust(10)+(str(j)+'%').rjust(4))
