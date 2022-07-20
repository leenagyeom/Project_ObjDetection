import os
import cv2
import numpy as np

img_path = "./raw_image/P1500"
lab_path = "./raw_image/P1500_labels"
img_list = os.listdir(img_path)
lab_list = os.listdir(lab_path)

for e, l in enumerate(lab_list, start=2486):
    nl = l.split('txt')[0][:-1]
    for i in img_list:
        ni = i.split('jpg')[0][:-1]
        if ni == nl :
            new_i = 'img_'+str(e)+'.png'
            new_l = 'img_'+str(e)+'.txt'
            os.rename(f"./{img_path}/{i}", f"./{img_path}/{new_i}")
            os.rename(f"./{lab_path}/{l}", f"./{lab_path}/{new_l}")
