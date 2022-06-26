import time
import easyocr
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
images_path = "images/tmp"
image_list = os.listdir(images_path)
start_time = time.time()
for img in image_list:
    result = reader.readtext(f'images/tmp/{img}')
    result_str = ""
    if result:
        for tmp_result in result:
            result_str = result_str + tmp_result[1] + " "
        result_str = img.split(".")[0].strip() + ": " + result_str
    else:
        result_str = img.split(".")[0].strip() + ": " + result_str
    print(result_str)
end_time = time.time()

dura_time = end_time - start_time
print(f"duration time: {dura_time}")
# img = cv2.imread("img_1.png")

# for detection in result1:
#     top_left = tuple(detection[0][0])
#     bottom_right = tuple(detection[0][2])
#     text = detection[1]
#     font = cv2.FONT_HERSHEY_SIMPLEX
#
#     img = cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 3)
#     img = cv2.putText(img, text, bottom_right, font, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
#
# plt.figure(figsize=(10, 10))
# plt.imshow(img)
# plt.show()

# print(result)
#
# print(type(result1))
# print(type(result1[0]))
# print(result1[0])
# print(result1[0][1])

# i = 0
# for tmp_result in result_list:
#
#     result_str = ""
#     if tmp_result:
#         for tmp_result1 in tmp_result:
#             result_str = result_str + tmp_result1[1] + " "
#         result_str = str(i) + ": " + result_str
#     else:
#         result_str = str(i) + ": " + result_str
#     print(result_str)
#     i += 1
# result_str1 = ""
# for tmp_result in result1:
#     result_str1 = result_str1 + tmp_result[1] + " "
# print(result1)

# result_str2 = ""
# for tmp_result in result2:
#     result_str2 = result_str2 + tmp_result[1] + " "

# print(result_str)
# print(result_str1)
# print(result_str2)
