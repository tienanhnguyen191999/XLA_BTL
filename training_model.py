import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.utils import np_utils
import os
import cv2
import random

mapping_char = { 
     '0' : 0,
     '1' : 1,
     '2' : 2,
     '3' : 3,
     '4' : 4,
     '5' : 5,
     '6' : 6,
     '7' : 7,
     '8' : 8,
     '9' : 9,
     'a' : 10,
     'b' : 11,
     'c' : 12,
     'd' : 13,
     'e' : 14,
     'f' : 15,
     'g' : 16,
     'h' : 17,
     'i' : 18,
     'j' : 19,
     'k' : 20,
     'l' : 21,
     'm' : 22,
     'n' : 23,
     'o' : 24,
     'p' : 25,
     'q' : 26,
     'r' : 27,
     's' : 28,
     't' : 29,
     'u' : 30,
     'v' : 31,
     'w' : 32,
     'x' : 33,
     'y' : 34,
     'z' : 35,
    }

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

# 1. data folder ----> array(list)
raw_data = []
for r,d,f in os.walk('training_data_checked'):
    for images in f:
        img = cv2.imread(r +"/"+ images,-1)
        trans_mask = img[:,:,3] == 0
        img[trans_mask] = [255, 255, 255, 255]
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        img = cv2.resize(img, (28,28), -1)
        
        raw_data.append([img,mapping_char[r[-1]]])  
random.shuffle(raw_data)

# 2. list -----> to numpy ----> reshape
images_data = []
labels_data = []
totalImageForTrain = 14000 # total 16k
for item in raw_data:
    images_data.append(item[0])
    labels_data.append(item[1])

images_train = np.asarray(images_data[:totalImageForTrain], dtype=np.uint8)
labels_train = np.asarray(labels_data[:totalImageForTrain], dtype=np.uint8)

images_val = np.asarray(images_data[totalImageForTrain:totalImageForTrain+1000], dtype=np.uint8)
labels_val = np.asarray(labels_data[totalImageForTrain:totalImageForTrain+1000], dtype=np.uint8)

images_test = np.asarray(images_data[totalImageForTrain+1000:], dtype=np.uint8)
labels_test = np.asarray(labels_data[totalImageForTrain+1000:], dtype=np.uint8)

# 3. Reshape lại dữ liệu cho đúng kích thước mà keras yêu cầu
images_train = images_train.reshape(images_train.shape[0], 28, 28, 1)
images_val = images_val.reshape(images_val.shape[0], 28, 28, 1)
images_test = images_test.reshape(images_test.shape[0], 28, 28, 1)

# 4. One hot encoding label (Y)
print('Dữ liệu y ban đầu ', labels_train[0])
labels_train = np_utils.to_categorical(labels_train, len(mapping_char))
labels_val = np_utils.to_categorical(labels_val, len(mapping_char))
labels_test = np_utils.to_categorical(labels_test, len(mapping_char))
print('Dữ liệu y sau one-hot encoding ',labels_train[0])

# 5. Định nghĩa model
model = Sequential()
 
# Thêm Convolutional layer với 32 kernel, kích thước kernel 3*3
# dùng hàm sigmoid làm activation và chỉ rõ input_shape cho layer đầu tiên
model.add(Conv2D(32, (3, 3), activation='sigmoid', input_shape=(28,28,1)))

# Thêm Convolutional layer
model.add(Conv2D(32, (3, 3), activation='sigmoid'))

# Thêm Max pooling layer
model.add(MaxPooling2D(pool_size=(2,2)))

# Flatten layer chuyển từ tensor sang vector
model.add(Flatten())

# Thêm Fully Connected layer với 128 nodes và dùng hàm sigmoid
model.add(Dense(128, activation='sigmoid'))

# Output layer với len(mapping_char) node và dùng softmax function để chuyển sang xác xuất.
model.add(Dense(len(mapping_char) , activation='softmax'))

# 6. Compile model, chỉ rõ hàm loss_function nào được sử dụng, phương thức 
# đùng để tối ưu hàm loss function.
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# 7. Thực hiện train model với data
model.fit(images_train, labels_train, validation_data=(images_val, labels_val),
          batch_size=32, epochs=10, verbose=1)

# 8. Lưu model
model.save("alphabet_predict_model.h5")

# 9. Đánh giá model với dữ liệu test set
score = model.evaluate(images_test, labels_test, verbose=0)
print(score)

# 10. Dự đoán ảnh
# img_test = images_test[17]
# cv2.imshow('test', img_test)
# cv2.waitKey(0)
# y_predict = model.predict(img_test.reshape(1,28,28,1))
# print('Giá trị dự đoán: ', reverse_mapping_char[(np.argmax(y_predict))])