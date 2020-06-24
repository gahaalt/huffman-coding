import sys

import utils

args = sys.argv

codefolder = args[1]
print(f'decoding: {codefolder}')

text, _, _ = utils.decode_codefolder(codefolder)

print(f'saving to output.txt')
with open('output.txt', 'w') as f:
    f.write(text)
