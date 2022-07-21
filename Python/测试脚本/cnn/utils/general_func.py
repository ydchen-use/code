import numpy as np


def mean_squared_error(y, t):
    """
    均方误差函数
    :param y:
    :param t:
    :return:
    """
    return 0.5 * np.sum((y-t)**2)


# t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
# y = [0.1 , 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
# s = mean_squared_error(np.array(y), np.array(t))
# print(s)


def cross_entropy_error(y, t):
    if y.ndim == 1:
        t = t.reshape(1, t.size)
        y = y.reshape(1, y.size)

    batch_size = y.shape[0]
    return -np.sum(t * np.log(1e-7 + y)) / batch_size

t = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]
y = [0.1 , 0.05, 0.6, 0.0, 0.05, 0.1, 0.0, 0.1, 0.0, 0.0]
s = cross_entropy_error(np.array(y), np.array(t))
print(s)


def step_function(x):
    """
    阶跃函数
    :param x:
    :return:
    """
    return np.maximum(0, x)


def sigmoid(x):
    """
    sigmoid函数
    :param x:
    :return:
    """
    return 1 / (1 + np.exp(-x))


def identify_function(x):
    return x


def softmax(x):
    c = np.max(x)
    exp_a = np.exp(x - c)  # 溢出对策
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a
    return y


if __name__ == "__main__":
    pass
