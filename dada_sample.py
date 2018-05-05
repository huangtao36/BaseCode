import numpy as np
import os
import random
from scipy import misc
import  matplotlib.pyplot as plt
from PIL import Image


def get_path_list(file_dir, fname):
    list = [ ]
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):
            if fname in file:
                list.append(os.path.join(root, file))


def make_dirs(paths):
    if isinstance(paths, list) and not isinstance(paths, str):
        for path in paths:
            mkdir(path)
    else:
        mkdir(paths)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def sample_sparse(img, percetage):
    sample = np.zeros(img.shape).astype(int)
    sample_num = int(percetage * np.count_nonzero(img > 0))
    coordinate = [ ]
    i = 0

    while(i < sample_num):
        rand_x = random.randint(0, img.shape[0]-1)
        rand_y = random.randint(0, img.shape[1]-1)
        if (rand_x, rand_y) not in coordinate:
            if img[rand_x, rand_y] > 0:
                sample[rand_x, rand_y] = img[rand_x, rand_y]
                coordinate.append((rand_x, rand_y))
                i += 1

    return sample


def sampling(source, sample):
    image_list = os.listdir(source)

    make_dirs(sample)

    for dir1 in image_list:

        imgpath = source + '/' + dir1
        print(imgpath)

        image = misc.imread(imgpath)

        sample_image = sample_sparse(image, 0.3)
        image2 = Image.fromarray(sample_image).convert('L')

        save_path = os.path.join(sample, dir1)
        image2.save(save_path)

    print("done.")


if __name__ == '__main__':

    source_dir = './dataset169/train/sparse'
    sample_dir = './dataset169/train/sparse0.3'

    sampling(source_dir, sample_dir)
