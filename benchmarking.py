import time
from sys import getsizeof

import huffman_canonical
import huffman_standard
import utils

# %%

with open('books/nietzsche.txt', 'r', encoding='utf-8') as f:
    book = f.read()

print('Compression Benchmark')
orgsize = getsizeof(book)
theoretical_size = utils.get_theoretical_size(book)
print(f'Original text size: {orgsize / 1024:.1f} kB!')
print(f'Original theoretical size: {theoretical_size / 1024:.1f} kB')
print()

freq = utils.get_symbol_frequency(book)

# %%
# standard (bez normalizacji drzewa) huffman
print('Naive Huffman')

tick = time.time()
cbook, codes = huffman_standard.build_and_encode(book, freq)
print(f'Coding time: {time.time() - tick:5.3f}s')

tick = time.time()
decbook = utils.decode_text_with_codes(cbook, codes)
print(f'Decoding time: {time.time() - tick:5.3f}s')

clen = len(cbook)
print(f'Encoded text size: {clen / 8 / 1024:.1f} kB!')
print(f'Encoded matches decoded: {decbook == book}')
print()

# %%
# kanoniczny huffman
print('Canonical Huffman')

tick = time.time()
cbook, codes = huffman_canonical.build_and_encode(book, freq)
print(f'Coding time: {time.time() - tick:5.3f}s')

tick = time.time()
decbook = utils.decode_text_with_codes(cbook, codes)
print(f'Decoding time: {time.time() - tick:5.3f}s')

clen = len(cbook)
print(f'Encoded text size: {clen / 8 / 1024:.1f} kB!')
print(f'Encoded matches decoded: {decbook == book}')
print()

# %%
