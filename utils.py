import math
import time
from collections import Counter
from sys import getsizeof


def get_theoretical_size_of_text(text):
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
    maxlen = max([len(x) for x in invcodes.keys()])
    otext = []
    act = ''

    for letter in text:
        if len(act) > maxlen:
            act = ''

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


def get_codebook_size(f):
    maxkey = max([len(v) for v in f.values()])
    bytes_per_number = math.ceil(maxkey / 8)
    return getsizeof(list(f.keys())) + bytes_per_number * len(f)


def code_to_codefolder(code, codebook, folder):
    import os
    if not os.path.exists(folder):
        os.makedirs(folder)

    with open(f'{folder}/code', 'wb') as file:
        byt = bytearray()
        for i in range(0, len(code), 8):
            value = int(code[i:i + 8], 2)
            byt.append(value)
        file.write(byt)

    fk = open(f'{folder}/codebook_keys', 'w')
    fv = open(f'{folder}/codebook_values', 'w')

    for k in codebook.keys():
        vsize = len(k)
        break

    print(vsize, file=fk, end='\n')
    for k, v in codebook.items():
        print(k, file=fk, end='')
        print(v, file=fv)


def decode_codefolder(folder):
    import os
    assert os.path.exists(folder)
    with open(f'{folder}/code', 'rb') as file:
        code = file.read()
        code = code.decode('charmap')

        strcode = []
        for ch in code:
            num = ord(ch)
            num = bin(num)[2:]
            num = '0' * (8 - len(num)) + num
            strcode.append(num)
        strcode = ''.join(strcode)

    fk = open(f'{folder}/codebook_keys', 'r')
    fv = open(f'{folder}/codebook_values', 'r')
    vsize = fk.readline()
    vsize = int(vsize.strip('\n'))

    codebook = {}
    for v in fv.readlines():
        key = fk.read(vsize)
        codebook[key] = v.strip('\n')

    decoded = decode_text_with_codes(strcode, codebook)
    return decoded, strcode, codebook
#
# import huffman
# book = open('data/alice_in_wonderland.txt', 'r').read()
# code, codebook = huffman.extended(book, block_length=3)
# code_to_codefolder(code, codebook, 'test')
# dbook, dcode, dcodebook = decode_codefolder('test')
