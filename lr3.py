import random

import numpy as np

from lr2 import int_to_bin_word_array, get_syndromes_first, find_index, encoding

# 3.3  Написать функцию формирования порождающей и проверочной матриц расширенного кода Хэмминга (𝟐^𝒓,𝟐^𝒓−𝒓−𝟏,𝟑) на основе параметра 𝒓, а также таблицы синдромов для всех однократных ошибок.
# 3.4. Провести исследование расширенного кода Хэмминга для одно-, двух-, трёх- и четырёхкратных ошибок для 𝒓=𝟐,𝟑,𝟒.

def get_g_and_h_hemming(r: int):
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


def check_mistakes_hemming(g, h, s, r):
    e = np.eye(g.shape[1], dtype=int)
    x = np.random.randint(0, 2, 2**r - r - 1)
    v = x @ g % 2  # сформировали слово
    for step in range(1, 4):
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
        g, h = get_g_and_h_hemming(r)
        s = get_syndromes_first(h)
        print('H:', g, sep='\n')
        print('H:', h, sep='\n')
        print('Таблица синдромов:', s, sep='\n')
        check_mistakes_hemming(g, h, s, r)


if __name__ == '__main__':
    # 3.1, 3.2
    simple_hemming()

