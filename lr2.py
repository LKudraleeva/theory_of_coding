import itertools
from matrix import distance
import numpy as np


def g_matrix(x: np.ndarray, k: int):
    g = np.eye(k, dtype=int)
    g = np.append(g, x, axis=1)
    return g


def h_matrix(x: np.ndarray, n: int, k: int):
    h = np.copy(x)
    h = np.append(h, np.eye(n - k, dtype=int), axis=0)
    return h


def get_syndromes_first(h: np.ndarray):
    syndromes = dict()
    for i in range(len(h)):
        syndromes[tuple(h[i])] = [i]
    return syndromes


def get_syndromes_second(h: np.ndarray, n: int):
    syndromes = dict()
    errors = np.eye(n, dtype=int)
    for i in range(len(h)):
        syndromes[tuple(h[i])] = [i]
    combs = list(itertools.combinations(range(0, n, 1), 2))
    for c in combs:
        e = errors[c[0]] + errors[c[1]]
        e = e @ h % 2
        syndromes[tuple(e)] = c
    return syndromes


def find_index(syndromes: dict, e: np.ndarray):
    return syndromes.get(tuple(e), [])


def encoding(word: np.ndarray, idx_errors: list):
    for e in idx_errors:
        word[e] += 1
        word[e] %= 2
    return word


def int_to_bin_word_array(size: int):
    bin_words = []
    for i in range(0, 2 ** size):
        bin_str = format(i, 'b')
        n = size - len(bin_str)
        if n > 0:
            bin_str = ''.zfill(n) + bin_str
        arr = [int(digit_char) for digit_char in bin_str]
        bin_words.append(arr)
    return np.asarray(bin_words)


def generate_x_second(n: int, k: int):
    d = 5
    x = int_to_bin_word_array(n - k)
    matrix = np.zeros((k, n - k), dtype=int)
    idx = []
    for i in range(x.shape[0]):
        if sum(x[i]) < d - 1:
            idx.append(i)
    x = np.delete(x, idx, axis=0)  # удаляем строки в которых меньше 4 единиц
    if x.shape[0] >= k:
        for c in itertools.combinations(range(0, x.shape[0], 1), k):
            flag = True
            # проверка сумм двух строк
            for c_2 in itertools.combinations(c, 2):
                if sum((x[c_2[0]] + x[c_2[1]]) % 2) < 3:
                    flag = False
                    break
            # проверка сумм трех строк
            if flag:
                for c_3 in itertools.combinations(c, 3):
                    if sum((x[c_3[0]] + x[c_3[1]] + x[c_3[2]]) % 2) < 2:
                        flag = False
                        break
            # проверка сумм четырех строк
            if flag:
                for c_4 in itertools.combinations(c, 4):
                    if sum((x[c_4[0]] + x[c_4[1]] + x[c_4[2]] + x[c_4[3]]) % 2) < 1:
                        flag = False
                        break
            # проверка расстояния
            if flag:
                matrix = []
                for index in c:
                    matrix.append(x[index])
                matrix = np.asarray(matrix)
                g = g_matrix(matrix, matrix.shape[0])
                if distance(g)[0] == d:
                    break
    return matrix


def first_part():
    n = 7
    k = 4
    x_first = np.array([[0, 1, 1],
                        [1, 0, 1],
                        [1, 1, 0],
                        [1, 1, 1]])
    print(distance(x_first))
    # 2.1 - порождающая матрица
    g = g_matrix(x_first, k)
    print('G:', g, sep='\n')
    print('d = ', distance(g)[0])
    print('t = ', distance(g)[1])

    # 2.2 - проверочная матрица
    h = h_matrix(x_first, n, k)
    print('H:', h, sep='\n')

    # 2.3 - таблица синдромов
    s = get_syndromes_first(h)
    print('Таблица синдромов:', s, sep='\n')

    # 2.4 - ввод однократной ошибки
    e = np.eye(n, dtype=int)
    v = np.array([1, 0, 1, 0]) @ g % 2
    print('\nСлово: ', v)
    v_e = (v + e[5]) % 2
    print('Слово с однократной ошибкой: ', v_e)
    b = v_e @ h % 2
    print('Синдром: ', b)
    idx_error = find_index(s, b)
    print('Ошибка в индексе: ', idx_error)
    v_e = encoding(v_e, idx_error)
    print('Слово после исправления ошибки: ', v_e)

    # 2.5 - ввод двукратной ошибки
    v = np.array([1, 0, 1, 0]) @ g % 2
    print('\nСлово: ', v)
    v_e = (v + e[2] + e[5]) % 2
    print('Слово с двукратной ошибкой: ', v_e)
    b = v_e @ h % 2
    print('Синдром: ', b)
    idx_error = find_index(s, b)
    print('Ошибка в индексе: ', idx_error)
    v_e = encoding(v_e, idx_error)
    print('Слово после исправления ошибки: ', v_e)


def second_part():
    # x_second = np.array([[0, 1, 1, 1, 1, 0, 1, 0, 0],
    #                      [1, 0, 0, 1, 1, 1, 0, 1, 0],
    #                      [1, 1, 1, 0, 0, 1, 0, 0, 1],
    #                      [0, 0, 0, 1, 1, 1, 1, 0, 0]])

    n = 13
    k = 4
    x_second = generate_x_second(n, k)
    # проверка существования матрицы
    if np.array_equal(np.zeros((k, n - k), dtype=int), x_second):
        print('Матрицы не существует')
    else:
        # 2.6 - порождающая матрица
        g = g_matrix(x_second, x_second.shape[0])
        print('G:', g, sep='\n')
        n = g.shape[1]
        print('N = ', n)
        k = g.shape[0]
        print('K = ', k)
        print('d = ', distance(g)[0])
        print('t = ', distance(g)[1])

        # 2.7 - проверочная матрица
        h = h_matrix(x_second, n, k)
        print('H:', h, sep='\n')

        # 2.8 - таблица синдромов
        s = get_syndromes_second(h, n)
        print('Таблица синдромов:', s, sep='\n')

        # 2.9 - ввод однократной ошибки
        e = np.eye(n, dtype=int)
        v = np.array([1, 0, 0, 0]) @ g % 2
        print('\nСлово: ', v)
        v_e = (v + e[5]) % 2
        print('Слово с однократной ошибкой: ', v_e)
        b = v_e @ h % 2
        print('Синдром: ', b)
        idx_error = find_index(s, b)
        print('Ошибка в индексе: ', idx_error)
        v_e = encoding(v_e, idx_error)
        print('Слово после исправления ошибки: ', v_e)

        # 2.10 - ввод двукратной ошибки
        v = np.array([1, 0, 0, 0]) @ g % 2
        print('\nСлово: ', v)
        v_e = (v + e[1] + e[5]) % 2
        print('Слово с двукратной ошибкой: ', v_e)
        b = v_e @ h % 2
        print('Синдром: ', b)
        idx_error = find_index(s, b)
        print('Ошибка в индексе: ', idx_error)
        v_e = encoding(v_e, idx_error)
        print('Слово после исправления ошибки: ', v_e)

        # 2.11 - ввод трехрактной ошибки
        v = np.array([1, 0, 0, 0]) @ g % 2
        print('\nСлово: ', v)
        v_e = (v + e[1] + e[5] + e[2]) % 2
        print('Слово с трехкратной ошибкой: ', v_e)
        b = v_e @ h % 2
        print('Синдром: ', b)
        idx_error = find_index(s, b)
        print('Ошибка в индексе: ', idx_error)
        v_e = encoding(v_e, idx_error)
        print('Слово после исправления ошибки: ', v_e)


if __name__ == '__main__':
    # first_part()
    second_part()

