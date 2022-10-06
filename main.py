from matrix import *


class LinearCode:
    def __init__(self, matrix):
        self.matrix = matrix
        self.g = ref(matrix)
        self.h = check_matrix(self.g)

    def shape_of_g(self):
        k = self.g.shape[0]
        n = self.g.shape[1]
        return n, k


def checking(g, h):
    words_by_sum = words_by_sum_g(g)
    print('All words by sum G:', words_by_sum, sep='\n')
    matrix = np.array([[0, 0, 0, 0, 0], [0, 0, 0, 0, 1], [0, 0, 0, 1, 0],
                       [0, 0, 0, 1, 1], [0, 0, 1, 0, 0], [0, 0, 1, 0, 1], [0, 0, 1, 1, 0],
                       [0, 0, 1, 1, 1], [0, 1, 0, 0, 0], [0, 1, 0, 0, 1], [0, 1, 0, 1, 0], [0, 1, 0, 1, 1],
                       [0, 1, 1, 0, 0], [0, 1, 1, 0, 1], [0, 1, 1, 1, 0], [0, 1, 1, 1, 1], [1, 0, 0, 0, 0],
                       [1, 0, 0, 0, 1], [1, 0, 0, 1, 0], [1, 0, 0, 1, 1], [1, 0, 1, 0, 0], [1, 0, 1, 0, 1],
                       [1, 0, 1, 1, 0], [1, 0, 1, 1, 1], [1, 1, 0, 0, 0], [1, 1, 0, 0, 1], [1, 1, 0, 1, 0],
                       [1, 1, 0, 1, 1], [1, 1, 1, 0, 0], [1, 1, 1, 0, 1], [1, 1, 1, 1, 0], [1, 1, 1, 1, 1]])
    words_by_multi = matrix @ array.g % 2
    words_by_multi = np.unique(words_by_multi, axis=0)
    print(' ')
    print('All words by multiplication on G:', words_by_multi, sep='\n')
    if np.array_equal(words_by_multi, words_by_sum):
        print('Arrays are equivalent')
    else:
        print('Arrays are not equivalent')
    # умножение всех кодовых слов на проверочную матрицу:
    check = words_by_multi @ h % 2
    print(' ')
    print('Multiplying codewords on checking matrix:', check, sep='\n')


if __name__ == '__main__':
    test_arr = np.array([[1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
                         [0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0],
                         [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
                         [1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0],
                         [0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0],
                         [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0]])
    array = LinearCode(test_arr)
    print('Shape of G: ', array.shape_of_g())
    G = array.g
    H = array.h
    print('G:', G, sep='\n')
    print('H:', H, sep='\n')

    checking(G, H)

    print('d = ', distance(G)[0])
    print('t = ', distance(G)[1])

    v = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1])
    # e1 = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])  # found
    e1 = np.array([0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0])  # not found

    res = (v + e1) @ H % 2
    if np.any(res) > 0:
        print(res, '- error')
    else:
        print(res, '- no error')
