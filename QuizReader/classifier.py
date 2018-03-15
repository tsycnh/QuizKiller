import cv2
import keras
import numpy as np
def preprocess_input(x):
    tmpx = ((x/255)-0.5)*2

    return tmpx

word_dict = open('source.txt').readlines()
images=[]
for i in range(24):
    img = cv2.imread('test'+str(i)+'.jpg')
    p_img = preprocess_input(img)
    images.append(p_img)

ttt = np.array(images)

keras.backend.clear_session()
model = keras.models.load_model('chnData_resnet.h5')
classes = model.predict(ttt,batch_size=24)
print(classes.shape)
for c in classes:
    index = np.argmax(c)
    print(index)
    print(word_dict[index])
# print(classes)