import keras
import cv2
import numpy as np
from PIL import Image
from utils import avg_method

model = keras.models.load_model('alphabet_predict_model.h5')
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
    
for i in range(1000,1200):
    file_path_erase_for_test = 'data/erase_noise/erase_noise_{}.png'.format(i)
    file_path_raw_for_test = 'data/origin/origin_{}.png'.format(i)
    avg_method(file_path_erase_for_test)
    result = ""
    for i in range(1,6):
        erase_img = cv2.imread('data/split/output_{}.png'.format(i),-1)
        trans_mask = erase_img[:,:,3] == 0
        erase_img[trans_mask] = [255, 255, 255, 255]
        erase_img = cv2.cvtColor(erase_img, cv2.COLOR_BGRA2GRAY)
        erase_img = cv2.resize(erase_img, (28,28), -1)
        predict = model.predict(erase_img.reshape(1,28,28,1))
        result += reverse_mapping_char[np.argmax(predict)]

    print(result)
    img = cv2.imread(file_path_raw_for_test,-1)
    trans_mask = img[:,:,3] == 0
    img[trans_mask] = [255, 255, 255, 255]
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    img_result = np.zeros((img.shape), dtype=np.uint8)
    cv2.putText(img_result,result,(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255))

    cv2.imshow('RAW', img)
    cv2.imshow('TEXT_PREDICT', img_result)
    cv2.waitKey()