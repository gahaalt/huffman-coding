from sortedcontainers import SortedList

import utils


def get_huffman_codes(freq):
    class Node:
        def __init__(self, prob, letter, lson=None, rson=None):
            self.letter = letter
            self.prob = prob
            self.lson = lson
            self.rson = rson

    codes = {key: str() for key in freq}
    nodes = [Node(v, letter=k) for k, v in freq.items()]
    nodes = SortedList(nodes, key=lambda x: (-x.prob, len(x.letter)))

    while len(nodes) > 1:
        v1 = nodes.pop()
        v2 = nodes.pop()

        for key in v1.letter:
            codes[key] += '0'
        for key in v2.letter:
            codes[key] += '1'

        new_node = Node(prob=v1.prob + v2.prob,
                        letter=v1.letter + v2.letter,
                        lson=v1,
                        rson=v2)
        nodes.add(new_node)

    codes = {key: code[::-1] for key, code in codes.items()}
    return codes


def build_and_encode(text, freq):
    codes = get_huffman_codes(freq)
    return utils.encode_text_with_codes(text, codes), codes
