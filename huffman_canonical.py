# %%
import time
from collections import Counter

from sortedcontainers import SortedList

import utils


# %%

def get_levels(freq):
    """
    Wewnętrznie tworzy drzewo, które zastępuje tablicą `leaves`, zawierającą
    liczby liści na kolejnych poziomach drzewa.
    :returns: tablica `levels`
    """

    class Node:
        def __init__(self, prob, creation_t=0, lson=None, rson=None):
            self.prob = prob
            self.lson = lson
            self.rson = rson
            self.creation_t = creation_t

    nodes = [Node(f) for f in freq.values()]
    nodes = SortedList(nodes, key=lambda x: (-x.prob, -x.creation_t))

    global_age = 1
    while len(nodes) > 1:
        v1 = nodes.pop()
        v2 = nodes.pop()

        new_node = Node(prob=v1.prob + v2.prob,
                        lson=v1,
                        rson=v2,
                        creation_t=global_age)
        nodes.add(new_node)
        global_age += 1

    # search the tree to find the leaves
    depth = 0
    leaves = []
    this_level = [nodes[0]]
    while this_level:
        new_level = []
        while this_level:
            node = this_level.pop()
            if not node.rson and not node.lson:
                leaves.append(depth)
            else:
                if node.rson:
                    new_level.append(node.rson)
                if node.lson:
                    new_level.append(node.lson)

        this_level = new_level
        depth += 1
    leaves = Counter(leaves)
    leaves = [leaves[k] for k in range(1, depth)]
    return leaves


test_input = '7777771523445666777777'
freq = utils.get_symbol_frequency(test_input)
leaves = get_levels(freq)
assert leaves == [1, 0, 2, 4]


# %%

def leaves_to_codes(levels):
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


codes = leaves_to_codes(leaves)

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

@utils.timer
def build_and_encode(text, freq):
    time0 = time.time()
    levels = get_levels(freq)
    tree_time = time.time() - time0

    only_codes = leaves_to_codes(levels)
    codes = match_freq_with_codes(freq, only_codes)

    time0 = time.time()
    encoded = utils.encode_text_with_codes(text, codes)
    enco_time = time.time() - time0

    return encoded, codes, tree_time, enco_time

# %%
