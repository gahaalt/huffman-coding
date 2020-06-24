import time
from sys import getsizeof

import matplotlib.pyplot as plt
import seaborn as sns

import huffman_canonical
import huffman_extended
import huffman_standard
import utils

sns.set()

# %%

with open('data/word2vec20k.txt', 'r', encoding='utf-8') as f:
    book = f.read()

sizes = {}

# %%

print('Compression Benchmark')
orgsize = getsizeof(book) / 1024 / 1024
theoretical_size = utils.get_theoretical_size_of_text(book) / 1024 / 1024

sizes['org'] = orgsize
sizes['theo'] = theoretical_size
print(f'Original text size: {orgsize:.1f} MB!')
print(f'Original theoretical size: {theoretical_size:.1f} MB')
print()

symbol_frequency = utils.get_symbol_frequency(book)

# %%
# standard (bez normalizacji drzewa) huffman
print('Naive Huffman')

cbook, codebook = huffman_standard.build_and_encode(book, symbol_frequency)
decbook = utils.decode_text_with_codes(cbook, codebook)

clen = len(cbook) / 8 / 1024 / 1024
sizes['naive'] = clen
print(f'Encoded text size: {clen:.1f} MB!')
print(f'Encoded matches decoded: {decbook == book}')
print()

# %%
# kanoniczny huffman
print('Canonical Huffman')

cbook, codebook, _, _ = huffman_canonical.build_and_encode(book, symbol_frequency)
decbook = utils.decode_text_with_codes(cbook, codebook)

clen = len(cbook) / 8 / 1024 / 1024
print(f'Encoded text size: {clen:.1f} MB!')
print(f'Encoded matches decoded: {decbook == book}')
print()

# %%
# rozszerzony huffmana z mnożeniem prawdopodobieństw

args = [1, 2, 3, 4, 5, 6]

sizes['extended'] = []
sizes['extendedB'] = []
sizes['extendedT1'] = []
sizes['extendedT2'] = []
for k in args:
    print(f'Extended Huffman, group size {k}')

    cbook, codebook, t1, t2 = huffman_extended.build_and_encode(book,
                                                                freq=symbol_frequency,
                                                                group_size=k)
    sizes['extendedT1'].append(t1)
    sizes['extendedT2'].append(t2)
    decbook = utils.decode_text_with_codes(cbook, codebook)

    clen = len(cbook) / 8 / 1024 / 1024
    cblen = utils.get_codebook_size(codebook) / 1024 / 1024

    sizes['extended'].append(clen)
    sizes['extendedB'].append(cblen + clen)
    print(f'Encoded text size: {clen:.1f} MB!')
    print(f'Codebook size: {cblen:.1f} MB')
    print(f'Summed size: {cblen + clen:.1f} MB')
    print(f'Encoded matches decoded: {decbook == book}')
    print()

# %%
# rozszerzony huffmana z wyliczaniem prawdopodobieństw

sizes['extended+'] = []
sizes['extended+B'] = []
sizes['extended+T1'] = []
sizes['extended+T2'] = []
for k in args:
    print(f'Extended Huffman+, group size {k}')

    cbook, codebook, t1, t2 = huffman_extended.build_and_encode(book,
                                                                group_size=k)
    sizes['extended+T1'].append(t1)
    sizes['extended+T2'].append(t2)
    decbook = utils.decode_text_with_codes(cbook, codebook)

    clen = len(cbook) / 8 / 1024 / 1024
    cblen = utils.get_codebook_size(codebook) / 1024 / 1024

    sizes['extended+'].append(clen)
    sizes['extended+B'].append(cblen + clen)
    print(f'Encoded text size: {clen:.1f} MB!')
    print(f'Codebook size: {cblen:.1f} MB')
    print(f'Summed size: {cblen + clen:.1f} MB')
    print(f'Encoded matches decoded: {decbook == book}')
    print()

# %%

args = range(1, len(sizes['extended']) + 1)

plt.figure(dpi=150)
plt.xticks(args)
plt.plot(args, sizes['extended'], label='probability derived from product')
plt.plot(args, sizes['extended+'], label='probability derived from data')
plt.ylabel('Code size (in MB)')
plt.xlabel('Extension length')
plt.legend()

plt.savefig('plots/extended.png')
plt.show()

# %%

plt.figure(dpi=150)
plt.xticks(args)
plt.plot(args, sizes['extendedB'], label='probability derived from product')
plt.plot(args, sizes['extended+B'], label='probability derived from data')
plt.ylabel('Code size (in MB)')
plt.xlabel('Extension length')
plt.legend()

plt.savefig('plots/extended_with_codebook.png')
plt.show()

# %%

plt.figure(dpi=150)
plt.xticks(args)
plt.plot(args, sizes['extended+T1'], label='time to create tree')
plt.plot(args, sizes['extended+T2'], label='time to code text')
plt.ylabel('Time taken on task')
plt.xlabel('Extension length')
plt.legend()

plt.savefig('plots/extended_time.png')
plt.show()

# %%
