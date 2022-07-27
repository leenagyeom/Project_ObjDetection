import os
import warnings
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
warnings.filterwarnings("ignore", category=UserWarning)

import torch
from PIL import Image, ImageFilter
import easyocr
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import time

path = './crops'

def easy_ocr (path) :
    reader = easyocr.Reader(['ko', 'en'], gpu=False)
    result = reader.readtext(path)
    read_result = result[0][1]
    read_confid = int(round(result[0][2], 2) * 100)
    return read_result, read_confid


def tess_ocr (path) :
    image = Image.open(path)
    text = pytesseract.image_to_string(image, lang='kor', config='--psm 4 --oem 3')
    text = text.rsplit('\n')[0]
    return text


def azure_ocr(path):
    subscription_key = "key"
    endpoint = "endpoint"
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

    img = open(path, "rb")
    read_response = computervision_client.read_in_stream(img, language="ko", raw=True)
    read_operation_location = read_response.headers["Operation-Location"]
    operation_id = read_operation_location.split("/")[-1]

    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                result = line.text
                # print(line.bounding_box)
    return result


# 학습된 모델 호출
model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5n_best.pt', force_reload=True)

# 이미지 불러오기
img = Image.open('../dataset/test/img_753950_1.jpg')  # PIL image
img = img.convert("L")

# 모델에 이미지 입력
results = model(img, size=640)

# results를 pandas로 정리
df = results.pandas().xyxy[0]
print(df)
'''
          xmin        ymin         xmax        ymax  confidence  class   name
0   116.761169  208.202805  1044.926025  767.356384    0.976881      0    car
1   359.405090  608.750916   566.712891  660.803223    0.876195      1  plate
2  1051.030151  484.713440  1102.585327  516.971680    0.750280      1  plate
'''

crops = results.crop(save=False)
# conf = (crop[0]['conf'].item() * 100)
print(crops)

for num, crop in enumerate(crops) :
    if 'plate' in crop['label'] :
        image = crop['im']
        im = Image.fromarray(image)
        im.save(os.path.join(path, f'plate_{num}.png'), 'png')

        if df['name'][0] == 'plate' :
            plate_name = df['name'][0]
            plate_conf = int((round(df['confidence'][0], 2)) * 100)
        else :
            plate_name = df['name'][1]
            plate_conf = int((round(df['confidence'][1], 2)) * 100)

        print("====== Crop Image Plate predict =======")
        print(f'{plate_name} 예측 확률 : {plate_conf}%')
        print("=======================================")

file_list = os.listdir(path)
for num, file in enumerate(file_list):
    azure = azure_ocr(f'{path}/{file}')
    print("\n===== Crop Image OCR Read - Azure =====")
    print(f'Azure OCR 결과    : {azure}')
    print("=======================================")
    result, confid = easy_ocr(f'{path}/{file}')
    print("===== Crop Image OCR Read - Easy ======")
    print(f'Easy OCR 결과     : {result}')
    print(f'Easy OCR 확률     : {confid}%')
    print("=======================================")
    tess = tess_ocr(f'{path}/{file}')
    print("=== Crop Image OCR Read - Tesseract ===")
    print(f'Tess OCR 결과     : {tess}')
    print("=======================================")
