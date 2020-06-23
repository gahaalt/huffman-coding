from sys import getsizeof

import huffman_canonical
import huffman_extended
import huffman_standard
import utils

# %%

with open('books/moby_dick.txt', 'r', encoding='utf-8') as f:
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

cbook, codes = huffman_standard.build_and_encode(book, freq)
decbook = utils.decode_text_with_codes(cbook, codes)

clen = len(cbook)
print(f'Encoded text size: {clen / 8 / 1024:.1f} kB!')
print(f'Encoded matches decoded: {decbook == book}')
print()

# %%
# kanoniczny huffman
print('Canonical Huffman')

cbook, codes = huffman_canonical.build_and_encode(book, freq)
decbook = utils.decode_text_with_codes(cbook, codes)

clen = len(cbook)
print(f'Encoded text size: {clen / 8 / 1024:.1f} kB!')
print(f'Encoded matches decoded: {decbook == book}')
print()

# %%
# rozszerzony huffmana z mnożeniem prawdopodobieństw

for k in [1, 2, 3, 5, 10]:
    print(f'Extended Huffman, group size {k}')
    cbook, codes = huffman_extended.build_and_encode(book, freq=freq, group_size=k)
    decbook = utils.decode_text_with_codes(cbook, codes)

    clen = len(cbook)
    print(f'Encoded text size: {clen / 8 / 1024:.1f} kB!')
    print(f'Encoded matches decoded: {decbook == book}')
    print()

# %%
# rozszerzony huffmana z wyliczaniem prawdopodobieństw

for k in [1, 2, 3, 5, 10]:
    print(f'Extended Huffman+, group size {k}')
    cbook, codes = huffman_extended.build_and_encode(book, group_size=k)
    decbook = utils.decode_text_with_codes(cbook, codes)

    clen = len(cbook)
    print(f'Encoded text size: {clen / 8 / 1024:.1f} kB!')
    print(f'Encoded matches decoded: {decbook == book}')
    print()

# %%
