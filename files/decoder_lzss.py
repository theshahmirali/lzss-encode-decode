# Name: Shah Mir Ali Bin Kamran

import sys

class HuffmanNode:
    def __init__(self, val, freq):
        self.val = val
        self.freq = freq
        self.left = None
        self.right = None

    def __init__(self):
        self.val = None
        self.freq = None
        self.left = None
        self.right = None


def to_binary(n):
    return "{0:b}".format(n)


def to_decimal(b):
    if b == "":
        return 0
    return int(b, 2)


def to_bit_string(buffer):
    res = ""
    for b in buffer:
        res += to_binary(b).zfill(8)
    return res


def elias_omega_decode(st):
    """
    Decode the elias encoding to number. Algorithm followed in the lectures and tutes.
    :param st: string in bits
    :return: the decoded number
    """
    i = 0
    num = st[0:1]
    length = 1
    while num and num[0] == "0":
        i += length
        num = "1" + num[1:]
        length = to_decimal(num) + 1
        num = st[i: i+length]
    return to_decimal(num), st[i+length:]


def build_huffman(huffman_codes, root):
    """
    :param huffman_codes: the dictionary
    :param root: the unique characters
    """
    for k, v in huffman_codes.items():
        cur = root
        for c in k:
            if c == "1":
                next = cur.right if cur.right is not None else HuffmanNode()
                cur.right = next
                cur = next
            else:
                next = cur.left if cur.left is not None else HuffmanNode()
                cur.left = next
                cur = next
        cur.val = v


def decode_huffman(st, root):
    """
    Decode the huffman encodes
    :param st: the input string
    :param root: the heap
    :return: the decoded string
    """
    cur = root
    for i, c in enumerate(st):
        if cur.val is not None:
            return cur.val, st[i:]
        if c == "1":
            cur = cur.right
        else:
            cur = cur.left
    return "\0", st


def decode(filename):
    """
    Decode the encoded file according to the specs.
    :param filename: the encdoded file
    :return: an output of decoded file
    """
    f = open(filename, "rb")
    buffer = f.read()
    bit_st = to_bit_string(buffer)
    dict_len, bit_st = elias_omega_decode(bit_st)
    huffman_codes = {}
    for i in range(dict_len):
        ch = chr(to_decimal(bit_st[:7]))
        bit_st = bit_st[7:]
        code_len, bit_st = elias_omega_decode(bit_st)
        code = bit_st[:code_len]
        bit_st = bit_st[code_len:]
        huffman_codes[code] = ch
    root = HuffmanNode()
    build_huffman(huffman_codes, root)
    number_of_fields, bit_st = elias_omega_decode(bit_st)
    fields = []
    res = ""
    for i in range(number_of_fields):
        bit, bit_st = bit_st[0], bit_st[1:]
        if bit == "1":
            ch, bit_st = decode_huffman(bit_st, root)
            res += ch
            fields.append((1, ch))
        else:
            offset, bit_st = elias_omega_decode(bit_st)
            size, bit_st = elias_omega_decode(bit_st)
            fields.append((0, offset, size))
            n = len(res)
            for j in range(size):
                res += res[n - offset + j]
    f = open("output_decoder_lzss.txt", "w")
    f.write(res)


if __name__ == "__main__":

    argument_00 = sys.argv[0]
    filename = sys.argv[1]
    decode(filename)
