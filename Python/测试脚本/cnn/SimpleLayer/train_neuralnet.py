import os, sys
sys.path.append(os.path.pardir)

import numpy as np
from ..datasets.mnist.mnist import load_mnist
from two_layers_net import TwoLayerNet


# 读入数据
(x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)

