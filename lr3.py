import random

import numpy as np

from lr2 import int_to_bin_word_array, get_syndromes_first, find_index, encoding


def hemming_matrix(r: int):
    t = int_to_bin_word_array(r)
    idx = []
    for i, row in enumerate(t):
        if sum(row) <= 1:
            idx.append(i)
    t = np.delete(t, idx, axis=0)  # удаляем строки в которых меньше 4 единиц
    t = np.flip(t, 0)
    g = np.append(np.eye(t.shape[0], dtype=int), t, axis=1)
    h = np.append(t, np.eye(r, dtype=int), axis=0)
    return g, h


def extend_hemming_matrix(r):
    g, h = hemming_matrix(r)
    h = np.append(h, [np.zeros(h.shape[1], dtype=int)], axis=0)
    h = np.append(h, np.ones((h.shape[0], 1), dtype=int), axis=1)
    g = np.append(g, np.zeros((g.shape[0], 1), dtype=int), axis=1)
    for i in range(g.shape[0]):
        if sum(g[i]) % 2 == 1:
            g[i][g.shape[1]-1] = 1
    return g, h


def check_mistakes_hemming(g, h, s, r, extend=False):
    e = np.eye(g.shape[1], dtype=int)
    x = np.random.randint(0, 2, 2**r - r - 1)
    v = x @ g % 2  # сформировали слово
    if extend:
        end = 5
    else:
        end = 4
    for step in range(1, end):
        print('\nСлово: ', v)
        index = random.sample(range(0, e.shape[0]), step)
        v_e = v
        for i in index:
            v_e = (v_e + e[i]) % 2
        print('Слово с', step, 'кратной ошибкой: ', v_e)
        b = v_e @ h % 2
        print('Синдром: ', b)
        idx_error = find_index(s, b)
        print('Ошибка в индексе: ', idx_error)
        v_e = encoding(v_e, idx_error)
        print('Слово после исправления ошибки: ', v_e)


def simple_hemming():
    for r in range(2, 5):
        print('r:', r, sep='\n')
        g, h = hemming_matrix(r)
        s = get_syndromes_first(h)
        print('G:', g, sep='\n')
        print('H:', h, sep='\n')
        print('Таблица синдромов:', s, sep='\n')
        check_mistakes_hemming(g, h, s, r)


def extend_hemming():
    r = 3
    g, h = extend_hemming_matrix(r)
    s = get_syndromes_first(h)
    print('G:', g, sep='\n')
    print('H:', h, sep='\n')
    print('Таблица синдромов:', s, sep='\n')
    check_mistakes_hemming(g, h, s, r, True)


if __name__ == '__main__':
    # 3.1, 3.2
    simple_hemming()
    # 3.3, 3.4
    extend_hemming()
