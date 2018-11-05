import os
import shutil
import ntpath
import numpy as np
from sklearn.model_selection import train_test_split


def get_path_list(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):  # 遍历文件目录下每一个文件
            L.append(os.path.join(root, file))
    return L


if __name__ == '__main__':
    trainApath = "./dataset/rgb"  # RGB图片
    trainBpath = "./dataset/groundtruth"  # semantic图片
    trainCpath = "./dataset/sparse"

    scene_array = np.arange(1, 1001)  # np.array(get_scene_from_txt(txtfile))
    image_name = np.arange(1, 1001)
    # 划分训练集和测试集  test_size（测试集比例）random_state（随机种子）
    X_train, X_test, Y_train, Y_test = train_test_split(scene_array, image_name, test_size=0.2, random_state=3)
    # 获得图片路径列表


    path_list = get_path_list(trainCpath)


    train_scene = []
    test_scene = []
    for i in range(len(path_list)):  # len(path_list)
        path = ''.join(path_list[i])   # ''.join()获取list的字符串值
        short_path = ntpath.basename(path)
        name = os.path.splitext(short_path)[0]
        # print(name)
        for s in Y_test:
            if s == int(name):
                # 复制图片到另一文件夹 shutil.copy(src, target)
                shutil.copy(path, './test/sparse')
                test_scene.append(path)
        if path in test_scene:
            continue
        shutil.copy(path, './train/sparse')
        train_scene.append(path)
        print(i)
    # 查看训练集与测试集图片个数
    print('train:', len(train_scene))
    print('test:', len(test_scene))
