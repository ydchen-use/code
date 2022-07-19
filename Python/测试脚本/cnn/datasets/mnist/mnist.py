import urllib.request

import os.path
import gzip
import pickle
import os
import numpy as np

url_base = "http://yann.lecun.com/exdb/mnist/"
key_file = {
    "train_img": "train-images-idx3-ubyte.gz",
    "train_label": "train-labels-idx1-ubyte.gz",
    "test_img": "t10k-images-idx3-ubyte.gz",
    "test_label": "t10k-labels-idx1-ubyte.gz"
}

dataset_dir = os.path.dirname(os.path.abspath(__file__))
print(f"dataset_dir : {dataset_dir}")
save_file = dataset_dir + "/mnist.pkl"

train_num = 60000
test_num = 10000
img_size = 784
img_dim = (1, 28, 28)


def download(file_name):
    file_path = dataset_dir + "/" + file_name
    if os.path.exists(file_path):
        return

    print("Downloading " + file_name + " ... ")
    urllib.request.urlretrieve(url_base + file_name, file_path)
    print("Done")


def download_mnist():
    for v in key_file.values():
        download(v)


def load_label(file_name):
    file_path = dataset_dir + "/" + file_name

    print("Converting " + file_name + " to NumPy Array ...")
    with gzip.open(file_path, "rb") as f:
        labels = np.frombuffer(f.read(), np.uint8, offset=8)
    print("Done")

    return labels


def load_img(file_name):
    file_path = dataset_dir + "/" + file_name

    print("Converting " + file_name + " to NumPy Array ...")
    with gzip.open(file_path, "rb") as f:
        data = np.frombuffer(f.read(), np.uint8, offset=16)
    data = data.reshape(-1, img_size)

    return data


def convert_numpy():
    dataset = {}
    dataset["train_img"] = load_img(key_file["train_img"])
    dataset["train_label"] = load_label(key_file["train_label"])
    dataset["test_img"] = load_img(key_file["test_img"])
    dataset["test_label"] = load_label(key_file["test_label"])

    return dataset


def init_mnist():
    download_mnist()
    dataset = convert_numpy()
    print("Creating pickle file ...")
    with open(save_file, "wb") as f:
        pickle.dump(dataset, f, -1)
    print("Done!")


if __name__ == "__main__":
    init_mnist()

