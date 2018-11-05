import numpy as np
import numpy as np
import os
from PIL import Image

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
                if count >= 1:
                    # first and last value for interpolation
                    u1 = u - count
                    u2 = u - 1
                    # set pixel to min depth
                    if u1 > 0 and u2 < width - 1:
                        d_ipol = predicted[v, u1 - 1] if predicted[v, u1 - 1] <= predicted[v, u2 + 1] else \
                        predicted[v, u2 + 1]
                        for u_curr in range(u1, u2 + 1, 1):
                            interpolated[v, u_curr] = d_ipol
                            # reset counter
                count = 0
            # otherwise increment counter
            else:
                count += 1
        # extrapolate to the left
        for u in range(width):
            if predicted[v, u] > 0:
                for u2 in range(u):
                    interpolated[v, u2] = predicted[v, u]
                break
        # extrapolate to the right
        for u in range(width - 1, -1, -1):
            if predicted[v, u] > 0:
                for u2 in range(u + 1, width - 1, 1):
                    interpolated[v, u2] = predicted[v, u]
                break
    # for each column do
    for u in range(width):
        # extrapolate to the top
        for v in range(height):
            if predicted[v, u] > 0:
                for v2 in range(v):
                    interpolated[v2, u] = predicted[v, u]
                break
        # extrapolate to the bottom
        for v in range(height - 1, -1, -1):
            if predicted[v, u] > 0:
                for v2 in range(v + 1, height - 1, 1):
                    interpolated[v2, u] = predicted[v, u]
                break
    return interpolated

def get_mask(input):
    mask = input > 0
    return mask.astype(float)

def calculate_depth_error(d_gt, d_pre):
    d_ipol = interpolateBackground(d_pre)
    # save interpolation image

    gt_mask = get_mask(d_gt)
    pixels = np.count_nonzero(gt_mask == 1)
    print(pixels)
    # print("pixels:", pixels)

    d_gt_m = d_gt * gt_mask
    d_ipol_m = d_ipol * gt_mask
    # print(d_gt_m)
    # print(d_ipol_m)

    d_err_inv = np.abs((1.0 / (d_gt_m/1000 + 10 ** -8) - 1.0 / (d_ipol_m/1000 + 10 ** -8)))
    # d_err_inv = np.abs(d_gt_m ** -1 - d_ipol_m ** -1)
    d_err_inv_squared = d_err_inv * d_err_inv
    # print(d_err)

    iRMSE_err = np.sqrt(np.sum(d_err_inv_squared) / pixels)
    iMAE_err = np.sum(d_err_inv) / pixels

    d_err_mm = np.abs(d_gt_m*1000 - d_ipol_m*1000)
    d_err_squared = d_err_mm * d_err_mm

    RMSE_err = np.sqrt(np.sum(d_err_squared) / pixels)
    MAE_err = np.sum(d_err_mm) / pixels

    return MAE_err, RMSE_err, iMAE_err, iRMSE_err

def normalize(image):
    max = np.max(image)
    min = np.min(image)
    #minA = A.min()
    #maxA = A.max()
    normalized = (image - min) / (max - min) * 255.0
    # normalized = np.minimum(np.maximum(image, 0), 255.0) / 255.0 * (max - min) + min
    return normalized

if __name__ == '__main__':
    image = np.array(Image.open("./real_B.png"), dtype=int)
    image1 = np.array(Image.open("./fake_B.png"), dtype=int)
    print(image)

    image_Complement = interpolateBackground(image1)
    print(image_Complement)

    mae_err, rmse_err, imae_err, irmse_err = calculate_depth_error(image, image_Complement)

    print("iRMSE: ", irmse_err)
    print("iMAE: ", imae_err)
    print("RMSE：",rmse_err)
    print("MAE: ", mae_err)

    image_normalize = normalize(image_Complement)

    image_done = Image.fromarray(image_normalize).convert('L')

    # image_done.show()


