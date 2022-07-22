import os
from sklearn.model_selection import train_test_split
import glob
import shutil

image_destination = "/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/test/images"
label_destination = "/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/test/labels"
os.makedirs(image_destination, exist_ok=True)
os.makedirs(label_destination, exist_ok=True)

image_path = "/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/train/images/"
label_path = "/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/train/labels/"

image_list = sorted(glob.glob(os.path.join(image_path, "*.png")))
label_list = sorted(glob.glob(os.path.join(label_path, "*.txt")))

train_x, valid_x, train_y, valid_y = train_test_split(image_list, label_list, test_size=0.2, random_state=7777)

# for i, j in zip(valid_x, valid_y):
#     shutil.move(i, image_destination)
#     shutil.move(j, label_destination)

print(len(glob.glob("/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/test/images/*")))
print(len(glob.glob("/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/test/labels/*")))
print(len(glob.glob("/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/train/images/*")))
print(len(glob.glob("/home/azureuser/cloudfiles/code/Users/leenagyeom_daeguai2022/detection/train/labels/*")))
