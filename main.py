import numpy as np


def change(A, i, j):
    A[[i, j]] = A[[j, i]]


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

    idx_arr = []
    for i in range(arr.shape[0]):
        if np.any(arr[i][:]) > 0:
            continue
        idx_arr.append(i)
    arr = np.delete(arr, idx_arr, axis=0)
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


class LinearCode:
    def __init__(self, matrix):
        self.matrix = matrix
        self.g = ref(matrix)
        self.h = self.check_matrix()

    def shape_of_g(self):
        k = self.g.shape[0]
        n = self.g.shape[1]
        return [n, k]

    def check_matrix(self):
        x = rref(self.g)
        print(x)
        n, k = self.shape_of_g()
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
        new_x = np.zeros((new_k, new_n), dtype=int)
        idx_x = 0
        idx_e = 0
        for i in range(len(new_x)):
            if i in lead:
                new_x[i] = x[idx_x]
                idx_x += 1
            else:
                new_x[i] = e[idx_e]
                idx_e += 1
        return new_x


if __name__ == '__main__':
    test_arr = np.array([[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                         [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
                         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                         [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
                         [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]])

    a = ref(test_arr)
    print(test_arr)
    print(a)
    array = LinearCode(test_arr)
    print(array.shape_of_g())
    G = array.g
    H = array.h
    print('G = ', G)
    print('H = ', H)
    # u = np.array([1, 0, 1, 1, 0])
    # v = u @ array.g % 2
    # print(v)
    # print(v @ array.h % 2)
    # #rref(test_arr)
