import time
import os
import easyocr
import cv2
import matplotlib.pyplot as plt

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

reader = easyocr.Reader(["ch_sim", "en"], gpu=True)
start_time = time.time()
result = reader.readtext("images/img_1.png")
end_time = time.time()

dura_time = end_time - start_time

print(dura_time)
print(result)

img = cv2.imread("images/img_1.png")

for detection in result:
    top_left = tuple(detection[0][0])
    bottom_right = tuple(detection[0][2])
    text = detection[1]
    font = cv2.FONT_HERSHEY_SIMPLEX

    img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)
    img = cv2.putText(img, text, bottom_right, font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

plt.figure(figsize=(10, 10))
plt.imshow(img)
plt.show()

