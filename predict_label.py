import keras
import cv2
import numpy as np
from PIL import Image
from add_label import avg_method

model = keras.models.load_model('alphabet_predict_model')
reverse_mapping_char = { 
         0 : '0' ,
         1 : '1' ,
         2 : '2' ,
         3 : '3' ,
         4 : '4' ,
         5 : '5' ,
         6 : '6' ,
         7 : '7' ,
         8 : '8' ,
         9 : '9' ,
         10: 'a' ,
         11: 'b' ,
         12: 'c' ,
         13: 'd' ,
         14: 'e' ,
         15: 'f' ,
         16: 'g' ,
         17: 'h' ,
         18: 'i' ,
         19: 'j' ,
         20: 'k' ,
         21: 'l' ,
         22: 'm' ,
         23: 'n' ,
         24: 'o' ,
         25: 'p' ,
         26: 'q' ,
         27: 'r' ,
         28: 's' ,
         29: 't' ,
         30: 'u' ,
         31: 'v' ,
         32: 'w' ,
         33: 'x' ,
         34: 'y' ,
         35: 'z' ,
        }
    
for i in range(20,30):
    file_path_for_test = 'data/erase_noise/erase_noise_{}.png'.format(i)
    avg_method(file_path_for_test)
    result = ""
    for i in range(1,6):
        img = cv2.imread('data/split/ouput_{}.png'.format(i),-1)
        trans_mask = img[:,:,3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        img = cv2.resize(img, (28,28), -1)
        predict = model.predict(img.reshape(1,28,28,1))
        result += reverse_mapping_char[np.argmax(predict)]

    print(result)
    img = cv2.imread(file_path_for_test,-1)
    trans_mask = img[:,:,3] == 0
    img[trans_mask] = [255, 255, 255, 255]
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
    cv2.imshow('origin', img)
    cv2.waitKey()