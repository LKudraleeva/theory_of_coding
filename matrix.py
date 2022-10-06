from functions import *


def ref(x: [[int]]) -> [[int]]:
    """Возвращает матрицу ступенчатого вида"""
    arr = np.copy(x)
    idx = 0
    flag = False
    for j in range(arr.shape[1]):
        for i in range(idx, arr.shape[0]):
            if np.any(arr[:, j]) > 0:
                if arr[i, j] == 1:
                    if not flag:
                        change(arr, i, idx)
                        flag = True
                    else:
                        arr[i] = (arr[i] + arr[idx]) % 2
        if flag:
            idx += 1
            flag = False

    arr = delete_null_rows(arr)
    return arr


def rref(x: [[int]]) -> [[int]]:
    """Возвращает приведенную матрицу ступенчатого вида"""
    arr = ref(x)
    for i in range(arr.shape[0] - 1, 0, -1):
        idx = 0
        for k in range(arr.shape[1]):
            if arr[i][k] == 1:
                idx = k
                break
        for j in range(0, i):
            if arr[j][idx] == 1:
                arr[j] = (arr[j] + arr[i]) % 2
    return arr


def check_matrix(g):
    """Возвращает проверочную матрицу"""
    x = rref(g)
    k = g.shape[0]
    n = g.shape[1]
    lead = []
    for i in range(k):
        for j in range(n):
            if x[i][j] == 1:
                lead.append(j)
                break
    x = np.delete(x, lead, axis=1)
    new_n = n - len(lead)
    new_k = n - len(lead) + k
    e = np.eye(new_n)
    h = np.zeros((new_k, new_n), dtype=int)
    idx_x = 0
    idx_e = 0
    for i in range(len(h)):
        if i in lead:
            h[i] = x[idx_x]
            idx_x += 1
        else:
            h[i] = e[idx_e]
            idx_e += 1
    return h


def words_by_sum_g(g):
    k = g.shape[0]
    n = g.shape[1]
    words_by_sum = np.array([])

    idx = []
    for i in range(k):
        idx.append(i)
    sub_idx = sub_sets(idx)

    for sub in sub_idx:
        w = np.zeros(n)
        if sub:
            for i in sub:
                w += g[i]
        w %= 2
        words_by_sum = np.append(words_by_sum, w)

    words_by_sum = np.resize(words_by_sum, (2 ** k, n))
    words_by_sum = words_by_sum.astype(int)
    words_by_sum = np.unique(words_by_sum, axis=0)
    return words_by_sum


def distance(g):
    k = g.shape[0]
    d = g.shape[1]
    for i in range(0, k - 1):
        for j in range(i + 1, k):
            temp = sum((g[i] + g[j]) % 2)
            if temp < d:
                d = temp
    return d, d - 1
