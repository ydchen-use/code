import numpy as np


def compute_min_edit_distance(str1, str2):
    """
    计算字符串之间的最小编辑距离
    :param str1:
    :param str2:
    :return:
    """
    # 计算两个字符串的长度
    str1_length = len(str1)
    str2_length = len(str2)

    # 以两个字符串的长度生成矩阵，保存距离
    distance_matrix = np.zeros((str1_length, str2_length))

    # 当str2为空时，
    for i in range(str1_length):
        distance_matrix[i][0] = i
    # 当str1为空时，
    for j in range(str2_length):
        distance_matrix[0][j] = j

    for i in range(1, str1_length):
        for j in range(1, str2_length):
            if str1[i] == str2[j]:
                diff = 0
            else:
                diff = 1
            distance_matrix[i][j] = min(distance_matrix[i - 1][j],
                                        distance_matrix[i][j - 1],
                                        distance_matrix[i - 1][j - 1]) + diff

    return distance_matrix[str1_length - 1][str2_length - 1]


if __name__ == "__main__":
    str1 = "abc"
    str2 = "adc"

    edit_dis = compute_min_edit_distance(str1, str2)
    print(edit_dis)
