# %%
from collections import Counter

from sortedcontainers import SortedList

import utils

# %%

with open('books/alice_in_wonderland.txt', 'r', encoding='utf-8') as f:
    book = f.read()


# %%

def get_levels(freq):
    """
    Wewnętrznie tworzy drzewo, które zastępuje tablicą `leaves`, zawierającą
    liczby liści na kolejnych poziomach drzewa.
    :returns: tablica `levels`
    """

    class Node:
        def __init__(self, prob, depth=0, creation_t=0, lson=None, rson=None):
            self.prob = prob
            self.lson = lson
            self.rson = rson
            self.depth = depth
            self.creation_t = creation_t

    leaves = [Node(f) for f in freq.values()]
    nodes = SortedList(leaves, key=lambda x: (-x.prob, -x.creation_t))

    global_age = 1
    while len(nodes) > 1:
        v1 = nodes.pop()
        v2 = nodes.pop()
        depth = max(v1.depth, v2.depth)
        v1.depth = depth
        v2.depth = depth
        new_node = Node(prob=v1.prob + v2.prob,
                        depth=depth + 1,
                        lson=v1,
                        rson=v2,
                        creation_t=global_age)
        nodes.add(new_node)
        global_age += 1

    root = nodes[0]
    counts = Counter([root.depth - 1 - leave.depth for leave in leaves])
    levels = [counts[i] for i in range(root.depth)]
    return levels


test_input = '1234455666777777777777'
freq = utils.get_symbol_frequency(test_input)
levels = get_levels(freq)
assert levels == [1, 0, 2, 4]


# %%

def levels_to_codes(levels):
    """
    W kodowaniu kanonicznym słowa kodowe moga byc nadanawe za pomocą tablicy levels.
    Niech D będzie najmniejszym indeksem, dla którego levels[D] != 0.
    Liść o największym numerze znajduje się na głębokości D i otrzymuje słowo kodowe
    złożone z D zer. Następnie nadawane są słowa kodowe wszystkim liściom,
    które znajdują się na tej samej głębokości, jeśli takie istnieją. Kolejno
    każdy liść otrzymuje słowo kodowe, który powstaje przez binarne dodanie 1.
    Po nadaniu słów kodowych wszystkim liściom o głębokości i, nadajemy je
    następnym liściom. Pierwszy liść na następnej niepustej głębokości otrzymuje
    słowo kodowe powstałe ze słowa kodowego poprzedniego liścia przez binarne
    dodanie 1 i dopisanie na końcu zer.
    """
    codes = []
    number = 2  # artifical 1 in binary representation, e.g. 100 instead of 00
    for L in levels:
        for _ in range(L):
            codes.append(bin(number)[3:])
            number += 1
        number *= 2
    return codes


codes = levels_to_codes(levels)
assert codes == ['0', '100', '101', '1100', '1101', '1110', '1111']


def match_freq_with_codes(freq, codes):
    """
    Dana jest tablica symboli i ich prawdopodobieństw, i tablica kodów.
    Najkrótsze kody nadajemy najbardziej prawdopodobnym symbolom.
    """
    sym2code = {}
    sorted_keys = sorted(freq, key=lambda x: freq[x])
    for key, code in zip(sorted_keys, codes[::-1]):
        sym2code[key] = code
    return sym2code


freq = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 3, 7: 12}
sym2code = match_freq_with_codes(freq, codes)
assert sym2code == {1: '1111', 2: '1110', 3: '1101', 4: '1100', 5: '101', 6: '100',
                    7: '0'}


# %%

def build_and_encode(text, freq):
    levels = get_levels(freq)
    only_codes = levels_to_codes(levels)
    codes = match_freq_with_codes(freq, only_codes)
    return utils.encode_text_with_codes(text, codes), codes

# %%
