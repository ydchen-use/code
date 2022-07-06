import mglearn
import pandas as pd
import numpy as np

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

# 导入数据库
iris_dataset = load_iris()

# 检查数据
print("keys of iris_dataset: \n{}".format(iris_dataset.keys()))

print(iris_dataset["DESCR"][:193] + "\n...")
print("\n")

# 要预测的花的品种
print("Target names: {}".format(iris_dataset["target_names"]))
print("\n")

# 对每一个特征的说明
print("Feature names: \n{}".format(iris_dataset["feature_names"]))
print("\n")

# data 数据的类型，numpy数组
print("Type of data: {}".format(type(iris_dataset["data"])))
print("\n")

# data数据的形状
print("Shape of data: {}".format(iris_dataset["data"].shape))
print("\n")

# target数据： 测量过的每朵花的品种
print("Type of target: {}".format(type(iris_dataset["target"])))
print("\n")

# target数据形状
print("Shape of target: {}".format(iris_dataset["target"].shape))
print("\n")

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(iris_dataset["data"], iris_dataset["target"], random_state=0)

# 训练集形状
print("X_train shape: {}".format(X_train.shape))
print("y_train shape: {}".format(y_train.shape))

# 测试集形状
print("X_test shape: {}".format(X_test.shape))
print("y_test shape: {}".format(y_test.shape))

# 利用X_train中的数据创建DataFrame
# 利用iris_dataset.feature_names中的字符串对数据列进行标记
iris_dataframe = pd.DataFrame(X_train, columns=iris_dataset.feature_names)

# 利用DataFrame创建散点图矩阵，按y_train着色
# grr = pd.plotting.scatter_matrix(iris_dataframe, c=y_train, figsize=(15, 15), marker="o",
#                                  hist_kwds={"bins": 20}, s=60, alpha=.8, cmap=mglearn.cm3)

# 实例化knn算法对象
knn = KNeighborsClassifier(n_neighbors=1)

# 调用knn对象的fit方法，基于训练集创建模型
knn.fit(X_train, y_train)

# 预测1朵新花
X_new = np.array([[5, 2.9, 1, 0.2]])
print("X_new shape: {}".format(X_new.shape))

# 调用knn对象的predict方法进行预测
prediction = knn.predict(X_new)
print("Prediction: {}".format(prediction))
print("Predicted target name: {}".format(iris_dataset["target_names"][prediction]))

# 考察模型的准确率
# 方法1
y_pred = knn.predict(X_test)
print("Test set predictions:\n {}".format(y_pred))

print("Test set score: {:.2f}".format(np.mean(y_pred == y_test)))

# 方法2  knn对象的score方法
print("Test set score: {:.2f}".format(knn.score(X_test, y_test)))

