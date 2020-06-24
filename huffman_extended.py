import math

import huffman_canonical
import utils


def get_extended_text(text, group_size=2):
    return [text[i * group_size:(i + 1) * group_size] for i in
            range(math.ceil(len(text) / group_size))]


@utils.timer
def build_and_encode(text, freq=None, group_size=1):
    grouped_text = get_extended_text(text, group_size)

    if freq is None:
        freq = utils.get_symbol_frequency(grouped_text)
    elif group_size != 1:
        real_freq = utils.get_symbol_frequency(grouped_text)

        for key in real_freq:
            prod = 1
            for l in key:
                prod *= freq[l]
            real_freq[key] = prod
        freq = real_freq

    return huffman_canonical.build_and_encode(grouped_text, freq)
