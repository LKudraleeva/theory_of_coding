import numpy as np


def encoding(g, a):
    return np.polymul(a, g) % 2


def decoding(n, k, G, syndromes, word_with_mistake):
    first_syndrome = (np.polydiv(word_with_mistake, G)[1] % 2).astype(int)
    e = np.array([0])
    x = np.array([1, 0])
    ans = None
    for i in range(1, k):
        first_syndrome = (np.polymul(x, first_syndrome)) % 2
        first_syndrome = (np.polydiv(first_syndrome, G)[1] % 2).astype(int)
        if list(first_syndrome) in syndromes:
            ans = i
            break
    if ans is not None:
        x_i = np.array(np.zeros(n - ans + 1, ), dtype=int)
        x_i[0] = 1
        e = np.polymul(x_i, first_syndrome)
        nul = np.zeros(n - e.shape[0], dtype=int)
        e = np.append(e[::-1], nul)
        print('Finding mistake:', e)
    return e


def word_equal(word, word_with_mistake, mistake):
    if not np.array_equal(mistake, np.array([0])):
        word_after_decoding = (word_with_mistake[::-1] + mistake) % 2
        print('After decoding:', word_after_decoding)
        if np.array_equal(word_after_decoding, word[::-1]):
            print('Arrays are equivalent')
        else:
            print('Arrays are not equivalent')
    else:
        print('Syndrome not found!')


def first_part():
    ar = np.array([1, 0, 0, 1])
    G = np.array([1, 1, 0, 1])
    word = encoding(ar, G)
    print('Word:', word[::-1])
    print('G: ', G[::-1])

    E = np.eye(7, dtype=int)
    print('Mistake:', E[2][::-1])
    word_with_mistake = (word + E[2]) % 2
    print('Word with mistake:', word_with_mistake[::-1])

    syndromes_1 = [[1]]
    error = decoding(7, 4, G, syndromes_1, word_with_mistake)
    word_equal(word, word_with_mistake, error)


def second_part():
    ar = np.array([1, 1, 0, 0, 0, 1, 0, 0, 1])
    G = np.array([1, 1, 1, 1, 0, 0, 1])
    word = encoding(ar, G)
    print('Word:', word[::-1])
    print('G: ', G[::-1])

    E = np.eye(15, dtype=int)
    print('Mistake:', (E[4] + E[6])[::-1])
    word_with_mistake = (word + E[4] + E[6]) % 2
    print('Word with mistake:', word_with_mistake[::-1])

    syndromes_2 = [[1], [1, 0, 1], [1, 1, 1], [1, 1]]
    error = decoding(15, 9, G, syndromes_2, word_with_mistake)
    word_equal(word, word_with_mistake, error)


if __name__ == '__main__':
    first_part()
    second_part()
