import numpy as np
import mglearn.datasets
import matplotlib.pyplot as plt

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_blobs
from sklearn.neighbors import KNeighborsClassifier

cancer = load_breast_cancer()

# 数据集的字段
print("cancer.keys: \n{}".format(cancer.keys()))
# dict_keys(['data', 'target', 'frame', 'target_names', 'DESCR', 'feature_names', 'filename'])

# 数据的形状
print("Cancer data shape: {}".format(cancer.data.shape))
# Cancer data shape: (569, 30)

# 恶性、良性数据
print("Sample counts per class:\n{}".format(
    {n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))
# {'malignant': 212, 'benign': 357}

# 生成测试集、训练集
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=66
)

# 训练集、测试集精度
training_accuracy = []
test_accuracy = []

# n_neighbors 取值从1到10
neighbors_settings = range(1, 11)

for n_neighbors in neighbors_settings:
    # 构建模型
    clf = KNeighborsClassifier(n_neighbors=n_neighbors)
    clf.fit(X_train, y_train)
    # 记录训练集精度
    training_accuracy.append(clf.score(X_train, y_train))
    # 记录泛化精度
    test_accuracy.append(clf.score(X_test, y_test))

plt.plot(neighbors_settings, training_accuracy, label="training accuracy")
plt.plot(neighbors_settings, test_accuracy, label="test accuracy")
plt.ylabel("Accuracy")
plt.xlabel("n_neighbors")
plt.legend()
plt.show()

# X, y = mglearn.datasets.make_forge()
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
#
# clf = KNeighborsClassifier(n_neighbors=3)
#
# clf.fit(X_train, y_train)
#
# # 对数据进行预测
# print("Test set predictions: {}".format(clf.predict(X_test)))
#
# # 评估模型的泛化能力好坏
# print("Test set accuracy: {:.2f}".format(clf.score(X_test, y_test)))
#
# fig, axes = plt.subplots(1, 3, figsize=(10, 3))
#
# for n_neighbors, ax in zip([1, 3, 9], axes):
#     # fit 方法返回对象本省，所以我们可以将实例化和你和放在一行代码中
#     clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)
#     mglearn.plots.plot_2d_separator(clf, X, fill=True, eps=0.5, ax=ax, alpha=.4)
#     mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
#     ax.set_title("{} neighbor(s)".format(n_neighbors))
#     ax.set_xlabel("feature 0")
#     ax.set_ylabel("feature 1")
# axes[0].legend(loc=3)
