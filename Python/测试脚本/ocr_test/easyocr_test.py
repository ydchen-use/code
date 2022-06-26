import logging
import easyocr


def text_detection(img_path):
    """
    图片文字识别
    :param img_path: 图片路径
    :return:
    """
    text_str = ""
    try:
        # 初始化检测模型
        reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
        # 拿到检测结果
        result_list = reader.readtext(img_path)
        for result in result_list:
            text_str = text_str + result[1] + " "
    except Exception as e:
        logging.exception(f"get text failed, error : {e}")

    return text_str

# reader = easyocr.Reader(["ch_sim", "en"], gpu=False)
# images_path = "images/tmp"
# image_list = os.listdir(images_path)
# result_list = []
# start_time = time.time()
# for img in image_list:
#     result = reader.readtext(f'images/tmp/{img}')
#     result_list.append(result)
# end_time = time.time()
#
# dura_time = end_time - start_time
# print(f"duration time: {dura_time}")
#
# for tmp_result in result_list:
#     result_str = ""
#     if tmp_result:
#         for tmp_result1 in tmp_result:
#             result_str = result_str + tmp_result1[1] + " "
#         print(result_str)

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
