import os
import cv2
import torch
from PIL import Image

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n_best.pt', force_reload=False)

im1 = Image.open('../dataset/test/img_735428_3.jpg')  # PIL image
print(im1)
exit()
im2 = cv2.imread('../dataset/test/img_756725_1.jpg', cv2.COLOR_BGR2RGB)  # OpenCV image (BGR to RGB)
imgs = [im1, im2]

results = model(imgs, size=640)  # includes NMS

car_name = results.pandas().xyxy[0]['name'][0]
car_conf = int((round(results.pandas().xyxy[0]['confidence'][0], 2)) * 100)
plate_name = results.pandas().xyxy[0]['name'][1]
plate_conf = int((round(results.pandas().xyxy[0]['confidence'][1], 2)) * 100)
print(f'{car_name} 예측 확률    :   {car_conf}%')
print(f'{plate_name} 예측 확률  :   {plate_conf}%')

crop = results.crop(save=False)
conf = (crop[0]['conf'].item() * 100)
if conf >= 70 :
    image = crop[0]['im']
    im = Image.fromarray(image)
    im.save('./crops/plate1.png', 'png')
