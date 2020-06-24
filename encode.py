import utils
import huffman
import sys

args = sys.argv

inputloc = args[1]
print(f'compressing: {inputloc}')

codefolder = args[2]
print(f'destination: {codefolder}')

with open(inputloc, 'r') as f:
    book = f.read()

code, codebook = huffman.extended(book, block_length=2)
utils.code_to_codefolder(code, codebook, codefolder)
