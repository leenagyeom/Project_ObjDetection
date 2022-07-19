import os
import cv2
import numpy as np

img_list = os.listdir("../raw_image/L500")
lab_list = os.listdir("../raw_image/L500_labels")

for e, i in enumerate(img_list, start=1):
    ni = i.split('jpg')[0][:-1]
    for l in lab_list:
        nl = l.split('txt')[0][:-1]
        if ni == nl :
            new_i = 'img_'+str(e)+'.png'
            new_l = 'img_'+str(e)+'.txt'
            os.rename(f"../raw_image/L500/{i}", f"../raw_image/L500_newimg/{new_i}")
            os.rename(f"../raw_image/L500_labels/{l}", f"../raw_image/L500_newlab/{new_l}")
