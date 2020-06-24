import huffman_extended
import huffman_canonical
import huffman_standard
import utils


def ambigous(text):
    assert isinstance(text, str)
    freq = utils.get_symbol_frequency(text)
    code, codebook = huffman_standard.build_and_encode(text, freq)
    return code, codebook


def canonical(text):
    assert isinstance(text, str)
    freq = utils.get_symbol_frequency(text)
    code, codebook, _, _ = huffman_canonical.build_and_encode(text, freq)
    return code, codebook


def extended(text, block_length=2, get_probs_from_data=True):
    assert isinstance(text, str)
    if not get_probs_from_data:
        freq = utils.get_symbol_frequency(text)
    else:
        freq = None

    code, codebook, _, _ = huffman_extended.build_and_encode(text, freq, block_length)
    return code, codebook


def decode(code, codebook):
    assert isinstance(code, str)
    return utils.decode_text_with_codes(code, codebook)
