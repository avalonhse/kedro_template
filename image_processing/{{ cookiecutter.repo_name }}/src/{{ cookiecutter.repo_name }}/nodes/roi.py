import numpy as np
from scipy.sparse import coo_matrix


def seg_to_roi(img):
    img = list(img.values())[0]

    print("type =", type(img))
    print("image =", img)

    peripheral_seg_val_arr = np.unique(
        np.concatenate([img[0, :], img[-1, :], img[:, 0], img[:, -1]])
    )
    peripheral_seg_val_3darr = np.expand_dims(peripheral_seg_val_arr, axis=0)
    central_flag_3darr = np.expand_dims(img, axis=2) != repeat_expand_dims(
        peripheral_seg_val_arr, n=2, axis=0
    )
    central_flag_2darr = np.all(central_flag_3darr, axis=2)
    if central_flag_2darr.max():
        central_coo = coo_matrix(central_flag_2darr)
        y_lower = int(np.percentile(central_coo.row, 5))
        y_upper = int(np.percentile(central_coo.row, 95))
        x_lower = int(np.percentile(central_coo.col, 5))
        x_upper = int(np.percentile(central_coo.col, 95))
        return np.array([x_lower, y_lower, x_upper, y_upper])
    else:
        h, w = img.shape
        return np.array([w // 2, h // 2, w // 2 + 1, h // 2 + 1])


def repeat_expand_dims(a, n=1, **kwargs):
    for i in range(n):
        a = np.expand_dims(a, **kwargs)
    return a
