import os
import warnings
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore", category=UserWarning)

import easyocr
import cv2
import torch
from PIL import Image

path = './crops'

def read_ocr (path) :
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    result = reader.readtext(path)
    return result

# 학습된 모델 호출
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n_best.pt', force_reload=False)

# 이미지 불러오기
img = Image.open('../dataset/test/img_735428_1.jpg')  # PIL image

# 모델에 이미지 입력
results = model(img, size=640)

# results를 pandas로 정리
df = results.pandas().xyxy[0]
'''
          xmin        ymin         xmax        ymax  confidence  class   name
0   116.761169  208.202805  1044.926025  767.356384    0.976881      0    car
1   359.405090  608.750916   566.712891  660.803223    0.876195      1  plate
2  1051.030151  484.713440  1102.585327  516.971680    0.750280      1  plate
'''

crops = results.crop(save=False)
# conf = (crop[0]['conf'].item() * 100)

for num, crop in enumerate(crops) :
    if 'plate' in crop['label'] and crop['conf'].item() * 100 > 78 :
        image = crop['im']
        im = Image.fromarray(image)
        im.save(os.path.join(path, f'plate_{num}.png'), 'png')

        plate_name = results.pandas().xyxy[0]['name'][1]
        plate_conf = int((round(results.pandas().xyxy[0]['confidence'][1], 2)) * 100)
        print(f'{plate_name} 예측 확률  :   {plate_conf}%')

file_list = os.listdir(path)
for num, file in enumerate(file_list):
    text = read_ocr(os.path.join(path, file))
    read_result = text[0][1]
    read_confid = int(round(text[0][2], 2) * 100)
    print(f'OCR 결과 : {read_result}')
    print(f'OCR 확률 : {read_confid}%')