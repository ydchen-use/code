import pytesseract as tess
import cv2
from imutils.object_detection import non_max_suppression
import argparse
import numpy as np
from PIL import Image

# image1 = Image.open("img_2.png")
# image1 = image1.convert("L")
# image1.save("image1_test.png")

# 将图片变为黑白图片
# image1 = Image.open("img_1.png")
# image1 = image1.convert("L")
# image1.save("image2_test.png")

# tesseract_version = tess.get_tesseract_version()
# tesseract_language = tess.get_languages()
# print(tesseract_version)
# print(tesseract_language)
#
image = cv2.imread("images/img_1.png")
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
text = tess.image_to_string(image_rgb, lang="chi_sim")
print(text)
print(type(text))
h, w, c = image.shape
boxes = tess.image_to_boxes(image)
for b in boxes.splitlines():
    b = b.split(" ")
    image = cv2.rectangle(image, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 1)

cv2.imshow("text detect", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

