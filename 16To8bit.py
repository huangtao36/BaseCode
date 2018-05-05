import numpy as np
import os
from PIL import Image


'''
获得文件路径列表
'''
def get_path_list(file_dir, fname):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):    # 遍历文件目录下每一个文件
            if fname in file:  # 判断是否包含指定字符串
                L.append(os.path.join(root, file))

if __name__ == '__main__':
    dir = './depth_val_000'  # 文件夹名
    dirs = os.listdir(dir)      #    ['(1).png', '(10).png', '(100).png', '(1000).png', '(1

    for dir1 in dirs:
        # print(dir1)
        imgpath = dir + '/' +dir1
        image = Image.open(imgpath)

        depth_png = np.array(image, dtype=int)

        depth = depth_png.astype(np.float) / 256.

        image2 = Image.fromarray(depth).convert('L')

        image2.save('./test/%s' % dir1)




