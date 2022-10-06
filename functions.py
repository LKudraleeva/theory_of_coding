import numpy as np


def change(x, i, j):
    x[[i, j]] = x[[j, i]]


def delete_null_rows(x):
    arr = np.copy(x)
    idx_arr = []
    for i in range(arr.shape[0]):
        if not np.any(arr[i][:]) > 0:
            idx_arr.append(i)
    arr = np.delete(arr, idx_arr, axis=0)
    return arr


def sub_sets(x):
    return subsets_recur([], sorted(x))


def subsets_recur(current, x):
    if x:
        return subsets_recur(current, x[1:]) + subsets_recur(current + [x[0]], x[1:])
    return [current]
