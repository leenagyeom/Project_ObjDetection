import os
import cv2
import numpy as np

image_list = os.listdir("../L500")
# label_list = os.listdir("./L500_labels")

# print(len(image_list), len(label_list))

def padding(img, set_size=640):
    percent = 1
    if(img.shape[1] > img.shape[0]):
        percent = set_size / img.shape[1]
    else:
        percent = set_size / img.shape[0]

    img = cv2.resize(img, dsize=(0, 0), fx=percent, fy=percent, interpolation=cv2.INTER_LINEAR)
    y, x, h, w = (0, 0, img.shape[0], img.shape[1])

    w_x = (set_size - (w - x)) / 2
    h_y = (set_size - (h - y)) / 2

    if (w_x < 0):
        w_x = 0
    elif (h_y < 0):
        h_y = 0

    M = np.float32([[1, 0, w_x], [0, 1, h_y]])
    img_re = cv2.warpAffine(img, M, (set_size, set_size))
    return img_re


for e, i in enumerate(image_list):
    img = cv2.imread('../L500/'+i, cv2.IMREAD_COLOR)
    new_img = padding(img)
    # cv2.imshow("new image", new_img)
    cv2.imwrite(f"../L500_padding/img_{e}.png", new_img)
    cv2.waitKey(0)
