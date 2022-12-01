from itertools import combinations, product
from statistics import mode
import numpy as np


def get_basis(cols):
    """Двоичное представление длины cols с обратным порядком байтов"""
    return [list(c)[::-1] for c in list(product([0, 1], repeat=cols))]


def f(indexes, u):
    """Функция f: возвращает 1, только когда v[i] = 0 для всех i из I"""
    if len(indexes) == 0 or np.all(np.asarray(u)[indexes] == 0):
        return 1
    else:
        return 0


def v(indexes, size):
    """Векторная форма для f"""
    return [f(indexes, b) for b in get_basis(size)]


def get_g(r, m):
    """Порождающая матрица"""
    return np.asarray([v(idx, m) for idx in get_all_indexes(r, m)])


def get_h(idx, m):
    """H: множество базисных слов, f от которых равна 1"""
    return [u for u in get_basis(m) if f(idx, u) == 1]


def get_complementary(idx, m):
    """I^c: комлементарное множество к множеству индексов"""
    return [i for i in range(m) if i not in idx]


def get_indexes(size, m):
    """Подмножество индексов мощности size"""
    return [list(comb) for comb in list(combinations(range(m - 1, -1, -1), size))]


def get_all_indexes(r, m):
    """Целое множество индексов"""
    index_array = []
    for i in range(0, r + 1):
        index_array.extend(get_indexes(i, m))
    return index_array


def f_with_t(idx, t, m):
    """Функция f I,t: действует как f, но с добавлением t"""
    return [int(np.array_equal(np.asarray(b)[idx], np.asarray(t)[idx])) for b in get_basis(m)]


def major(w, h, idx, m):
    """Возвращает значение мажорантного декодирования для индекса"""
    c = get_complementary(idx, m)
    v_array = [f_with_t(c, u, m) for u in h]
    ans = []
    for _v in v_array:
        ans.append(np.dot(np.asarray(_v), np.asarray(w)) % 2)
    return mode(ans)


def encoding(w, r, m, g):
    """Алгоритм декодирования"""
    a = np.zeros((g.shape[0]), dtype=int)
    mas = get_all_indexes(r, m)
    for step in range(r, -1, -1):
        indexes = get_indexes(step, m)
        first = []
        for idx in indexes:
            H = get_h(idx, m)
            first.append(major(w, H, idx, 4))
        pos = mas.index(indexes[0])   # первая позиции в массиве
        for i in range(0, len(first)):
            a[i + pos] = first[i]
        if step != 0:
            w = (a.T @ np.asarray(g) + w) % 2
        else:
            w = a.T @ np.asarray(g) % 2
        print('Word after', abs(step - r - 1), 'encoding:', w)
    return w


if __name__ == '__main__':
    G = get_g(2, 4)
    print('G:', G)
    mes = np.array([0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    print('Message:', mes)
    word_without_mistake = mes @ G % 2
    print('Word without mistake: ', word_without_mistake)
    E = np.eye(16, dtype=int)
    print('Mistake: ', E[4])
    word_with_mistake = (word_without_mistake + E[4]) % 2
    print('Word with mistake: ', word_with_mistake)
    word = encoding(word_with_mistake, 2, 4, G)
