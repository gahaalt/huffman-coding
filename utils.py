import time
from collections import Counter

import math


def get_theoretical_size(text):
    num_unique = len(set(text))
    bits_per_symbol = math.ceil(math.log2(num_unique))
    return int(math.ceil(len(text) * bits_per_symbol / 8))


def get_symbol_probs(text):
    """
    :return: a dictionary with symbols as keys and float probs as values
    """
    counts = Counter(text)
    sums = sum(counts.values())
    freq = {key: value / sums for key, value in counts.items()}
    return freq


def get_symbol_frequency(text):
    """
    :return: a dictionary with symbols as keys frequency as values
    """
    return Counter(text)


def encode_text_with_codes(text, codes):
    encoded = []
    for letter in text:
        assert letter in codes
        encoded.append(codes[letter])
    return ''.join(encoded)


def decode_text_with_codes(text, codes):
    invcodes = {value: key for key, value in codes.items()}
    otext = []
    act = ''
    for letter in text:
        act += letter
        if act in invcodes:
            otext.append(invcodes[act])
            act = ''
    return ''.join(otext)


def timer(func):
    def wrapper(*args, **kwargs):
        tick = time.time()
        rets = func(*args, **kwargs)
        print(f'{func.__module__} time: {time.time() - tick:5.3f}s')
        return rets

    return wrapper
