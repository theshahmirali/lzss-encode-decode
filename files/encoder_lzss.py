# Name: Shah Mir Ali Bin Kamran

import sys
from collections import Counter
from queue import PriorityQueue

counter = 0

class HuffmanNode:
    def __init__(self, val, freq):
        self.val = val
        self.freq = freq
        self.left = None
        self.right = None
        global counter
        self.totalCount = counter
        counter += 1

    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq
        return self.totalCount < other.totalCount


def to_binary(n):
    return "{0:b}".format(n)


def to_decimal(b):
    return int(b, 2)


def elias_omega_encode(n):
    """
    Encodes in Elias compression when given numbers. Algorithm followed in the lectures and tutes.
    :param n:
    :return: the encoded numbers
    """
    st = to_binary(n)
    res = st[:]
    while len(st) > 1:
        d = len(st) - 1
        st = to_binary(d)
        st = "0" + st[1:]
        res = st + res
    return res


def huffman_encode(unique_characters):
    """
    The heap for huffman encoding.
    :param unique_characters: the unique characters
    :return: the encoding in huffman form
    """
    q = PriorityQueue()
    for c, k in sorted(unique_characters.items(), key=lambda x: x[1]):
        q.put(HuffmanNode(c, k))
    while q.qsize() != 1:
        a = q.get()
        b = q.get()
        obj = HuffmanNode('\0', a.freq + b.freq)
        obj.left = a
        obj.right = b
        q.put(obj)

    root = q.get()
    return root


def dfs(root, huffman_codes, st=""):
    """
    :param root: the encoded unique characters
    :param huffman_codes: the dictionary
    """
    if root is not None:
        if root.val != '\0':
            huffman_codes[root.val] = st
        dfs(root.left, huffman_codes, st+"0")
        dfs(root.right, huffman_codes, st+"1")


# def compress_lz77(st, w, l):
#     i = 0
#     tuples = []
#     while i < len(st):
#         left = max(0, i-l)
#         right = i + w
#         index = 0
#         longestMatch = 0
#         nextCharacter = st[i]
#         nextIndex = i+1
#         for j in range(1, w+1):
#             ind = st[left:right].index(st[i:i+j])
#             if ind < min(i, l):
#                 index = ind
#                 longestMatch = j
#                 nextCharacter = st[i+j] if i+j < len(st) else "\0"
#                 nextIndex = i+j+1
#         tuples.append((i - index - left, longestMatch, nextCharacter))
#         i = nextIndex
#     return tuples


def compress_lzss(st, w, l):
    """
    Encodes the text in LZSS compression. Algorithm followed in the lectures and tutes.
    :param st: the imput text
    :param w: search window
    :param l: lookahead buffer
    :return: an array compressed in the form of lzss
    """
    i = 0
    tuples = []
    while i < len(st):
        left = max(0, i-l)
        right = i + w
        index = 0
        longestMatch = 0
        nextCharacter = st[i]
        nextIndex = i+1
        for j in range(1, w+1):
            ind = st[left:right].index(st[i:i+j])
            if ind < min(i, l):
                index = ind
                longestMatch = len(st[i:i+j])
                nextCharacter = st[i+j-1] if i+j-1 < len(st) else st[-1]
                nextIndex = i+j
        if longestMatch < 2:
            tuples.append((1, nextCharacter))
        elif longestMatch == 2:
            tuples.append((1, st[nextIndex-2]))
            tuples.append((1, nextCharacter))
        else:
            tuples.append((0, i - index - left, longestMatch))
        i = nextIndex
    return tuples


def encode(filename, W, L, outputName):
    """
    Encodes the file input using the appropriately as mentioned in the specs.
    :param filename: the input file
    :param W: search window
    :param L: lookahead buffer
    :param outputName: the file to output to
    :return: an output file which is encoded
    """
    f = open(filename, "r")
    inputText = f.readline()
    uniqueCharacters = Counter(inputText)
    header = ""
    header += elias_omega_encode(len(uniqueCharacters))
    huffman_codes = {}
    dfs(huffman_encode(uniqueCharacters), huffman_codes)
    for k, v in sorted(huffman_codes.items()):
        header += (to_binary(ord(k)).zfill(7))
        header += elias_omega_encode(len(v))
        header += v
    lzss_fields = compress_lzss(inputText, W, L)
    data = ""
    data += elias_omega_encode(len(lzss_fields))
    for t in lzss_fields:
        bit = t[0]
        data += str(bit)
        if bit:
            data += huffman_codes[t[1]]
        else:
            data += elias_omega_encode(t[1]) + elias_omega_encode(t[2])
    data = header + data

    length = len(data) + 8 - (len(data) % 8)
    data = data.ljust(length, "0")
    i = 0
    buffer = bytearray()
    while i < len(data):
        buffer.append(int(data[i:i + 8], 2))
        i += 8
    with open(outputName, 'wb') as f:
        f.write(buffer)


if __name__ == "__main__":

    argument_00 = sys.argv[0]

    filename = sys.argv[1]
    W = int(sys.argv[2])
    L = int(sys.argv[3])
    outputName = "output_encoder_lzss.bin"
    encode(filename, W, L, outputName)
