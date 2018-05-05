#!/usr/bin/python

from PIL import Image
import numpy as np


def depth_read(filename):
    # loads depth map D from png file
    # and returns it as a numpy array,
    # for details see readme.txt

    depth_png = np.array(Image.open(filename), dtype=int)
    print(np.max(depth_png))
    # make sure we have a proper 16bit depth map here.. not 8bit!
    assert(np.max(depth_png) > 255)

    depth = depth_png.astype(np.float) / 256.

    depth[depth_png == 0] = -1.
    return depth


depth = depth_read('000006_10.png')
print(np.max(depth))
print(np.min(depth))