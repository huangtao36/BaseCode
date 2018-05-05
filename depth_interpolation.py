import os
import ntpath
import numpy as np
from PIL import Image
import cv2
from numpy import random


def get_ipol_value(temp, v, u, k):
    height = temp.shape[0]
    width = temp.shape[1]
    if v < k:
        if u < k:
            ipol = np.sum(temp[0:v+k+1, 0:u+k+1]) / np.count_nonzero(temp[0:v+k+1, 0:u+k+1] > 0)
        elif u > width-k-1:
            ipol = np.sum(temp[0:v+k+1, u-k:width]) / np.count_nonzero(temp[0:v+k+1, u-k:width] > 0)
        else:
            ipol = np.sum(temp[0:v+k+1, u-k:u+k+1]) / np.count_nonzero(temp[0:v+k+1, u-k:u+k+1] > 0)
    elif v > height-k-1:
        if u < k:
            ipol = np.sum(temp[v-k:height, 0:u+k+1]) / np.count_nonzero(temp[v-k:height, 0:u+k+1] > 0)
        elif u > width-k-1:
            ipol = np.sum(temp[v-k:height, u-k:width]) / np.count_nonzero(temp[v-k:height, u-k:width] > 0)
        else:
            ipol = np.sum(temp[v-k:height, u-k:u+k+1]) / np.count_nonzero(temp[v-k:height, u-k:u+k+1] > 0)
    else:
        if u < k:
            ipol = np.sum(temp[v-k:v+k+1, 0:u+k+1]) / np.count_nonzero(temp[v-k:v+k+1, 0:u+k+1] > 0)
        elif u > width-k-1:
            ipol = np.sum(temp[v-k:v+k+1, u-k:width]) / np.count_nonzero(temp[v-k:v+k+1, u-k:width] > 0)
        else:
            ipol = np.sum(temp[v-k:v+k+1, u-k:u+k+1]) / np.count_nonzero(temp[v-k:v+k+1, u-k:u+k+1] > 0)
    return ipol


def get_mask(input):
    mask = input > 0
    return mask.astype(float)


def normalize(A, minout, maxout):
    minA = A.min()
    maxA = A.max()
    normalized = (A - minA)/(maxA - minA)*(maxout - minout) + minout
    return normalized


# interpolate all missing (=invalid) depths
def interpolateBackground(predicted):

    height = predicted.shape[0]
    width = predicted.shape[1]
    interpolated = predicted.copy()

    # for each row do
    for v in range(height):
        # init counter
        count = 0
        # for each pixel do
        for u in range(width):
            # if depth valid
            if predicted[v, u] > 0:
                # at least one pixel requires interpolation
                if (count >= 1) and (count <= 3):
                    # first and last value for interpolation
                    u1 = u-count
                    u2 = u-1
                    # set pixel to min depth
                    if u1 > 0 and u2 < width-1:
                        d_ipol = predicted[v, u1-1] if predicted[v, u1-1] < predicted[v, u2+1] else predicted[v, u2+1]
                        for u_curr in range(u1, u2+1, 1):
                            if d_ipol == 0.0:
                                print(v)
                                d_ipol = predicted[v, u_curr - 1]
                            interpolated[v, u_curr] = d_ipol
                    # reset counter
                count = 0
            # otherwise increment counter
            else:
                count += 1
        # # extrapolate to the left
        # for u in range(width):
        #     if predicted[v, u] > 0:
        #         for u2 in range(u):
        #             interpolated[v, u2] = predicted[v, u]
        #         break
        # # extrapolate to the right
        # for u in range(width-1, -1, -1):
        #     if predicted[v, u] > 0:
        #         for u2 in range(u+1, width, 1):
        #             interpolated[v, u2] = predicted[v, u]
        #         break
    # for each column do
    for u in range(width):
        # init counter
        count_v = 0
        # for each pixel do
        for v in range(height):
            # if depth valid
            if predicted[v, u] > 0:
                # at least one pixel requires interpolation
                if count_v == 1:
                    # first and last value for interpolation
                    v1 = v - count_v
                    v2 = v - 1
                    # set pixel to min depth
                    if v1 > 0 and v2 < height - 1:
                        d_ipol = predicted[v1 - 1, u] if predicted[v1 - 1, u] < predicted[v2 + 1, u] else predicted[
                            v2 + 1, u]
                        for v_curr in range(v1, v2 + 1, 1):
                            if d_ipol == 0.0:
                                print(v)
                                d_ipol = predicted[v_curr - 1, u]
                            interpolated[v_curr, u] = d_ipol
                            # reset counter
                count_v = 0
            # otherwise increment counter
            else:
                count_v += 1
    # for u in range(width):
    #     # init counter
    #     count_v = 0
    #     # extrapolate to the top
    #     for v in range(height):
    #         if predicted[v, u] > 0:
    #             if (count_v >= 1) and (count_v <= 3):
    #                 for v2 in range(v):
    #                     interpolated[v2, u] = predicted[v, u]
    #                 break
    #             count_v = 0
    #         # otherwise increment counter
    #         else:
    #             count_v += 1
    #     # extrapolate to the bottom
    #     for v in range(height-1, -1, -1):
    #         if predicted[v, u] > 0:
    #             for v2 in range(v+1, height, 1):
    #                 interpolated[v2, u] = predicted[v, u]
    #             break
    return interpolated


def get_path_list(file_dir, fname):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in sorted(files):    # 遍历文件目录下每一个文件
            if fname in file:  # 判断是否包含指定字符串
                L.append(os.path.join(root, file))
    return L


if __name__ == '__main__':
    img_dir = "./dataset_800_200_expand/test/groundtruth"
    img_list = get_path_list(img_dir, "png")
    print("image: ", len(img_list))

    for i in range(len(img_list)):
        img_path = ''.join(img_list[i])   # ''.join()获取list的字符串值
        # 获取图片名
        short_path = ntpath.basename(img_path)
        name = os.path.splitext(short_path)[0]

        img = Image.open(img_path)
        img_npy = np.array(img)
        # print("_________ground truth__________")
        # print(np.count_nonzero(img_npy == 0))
        # print(img_npy[110:120, 10:20])
        ipol = interpolateBackground(img_npy)
        ipol = interpolateBackground(ipol)
        # kernel_size = (3, 3)
        # sigma = 1.5
        # ipol = cv2.GaussianBlur(ipol, kernel_size, sigma)
        ipol_npy = np.array(ipol)
        # print("_________ipol__________")
        # print(np.count_nonzero(ipol_npy == 0))
        # print(ipol_npy[110:120, 10:20])
        ipols = Image.fromarray(ipol_npy)
        if ipols.mode != 'L':
            ipols = ipols.convert('L')
        ipols.save("./dataset_800_200_expand/test/gt/%s.png" % name)
        print(i)

