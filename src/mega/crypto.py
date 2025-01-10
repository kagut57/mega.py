from Crypto.Cipher import AES
import json
import base64
from base64 import b64encode, b64decode
import struct
import binascii
import random
import sys

# Python3 compatibility
if sys.version_info < (3, ):

    def makebyte(x):
        return x

    def makestring(x):
        return x
else:
    import codecs

    def makebyte(x):
        return codecs.latin_1_encode(x)[0]

    def makestring(x):
        return codecs.latin_1_decode(x)[0]


def aes_cbc_encrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.encrypt(data)


def aes_cbc_decrypt(data, key):
    aes_cipher = AES.new(key, AES.MODE_CBC, makebyte('\0' * 16))
    return aes_cipher.decrypt(data)


def aes_cbc_encrypt_a32(data, key):
    return str_to_a32(aes_cbc_encrypt(a32_to_str(data), a32_to_str(key)))


def aes_cbc_decrypt_a32(data, key):
    return str_to_a32(aes_cbc_decrypt(a32_to_str(data), a32_to_str(key)))


def str_to_a32(b):
    if isinstance(b, str):
        return str_to_a32(b.encode('utf8'))
    if len(b) % 4:
        b += b'\0' * (4 - len(b) % 4)
    return [(int.from_bytes(b[i:i + 4], byteorder='big')) 
            for i in range(0, len(b), 4)]

def prepare_key(a):
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for r in range(0x10000):
        for j in range(0, len(a), 4):
            key = [0, 0, 0, 0]
            for i in range(4):
                if i + j < len(a):
                    key[i] = a[i + j]
            for i in range(4):
                pkey[i] ^= key[i]
    return pkey

def stringhash(s, aeskey):
    s32 = str_to_a32(s)
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for _ in range(0x4000):
        for j in range(0, len(h32), 4):
            key = [0, 0, 0, 0]
            for k in range(4):
                if j + k < len(h32):
                    key[k] = h32[j + k]
            for k in range(4):
                h32[j + k] ^= aeskey[k]
    return base64_url_encode(bytes(str_to_a32(str(h32))))


def encrypt_key(a, key):
    return sum((aes_cbc_encrypt_a32(a[i:i + 4], key)
                for i in range(0, len(a), 4)), ())


def decrypt_key(a, key):
    return sum((aes_cbc_decrypt_a32(a[i:i + 4], key)
                for i in range(0, len(a), 4)), ())


def encrypt_attr(attr, key):
    attr = makebyte('MEGA' + json.dumps(attr))
    if len(attr) % 16:
        attr += b'\0' * (16 - len(attr) % 16)
    return aes_cbc_encrypt(attr, a32_to_str(key))


def decrypt_attr(attr, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = makestring(attr)
    attr = attr.rstrip('\0')
    return json.loads(attr[4:]) if attr[:6] == 'MEGA{"' else False


def a32_to_str(a):
    return struct.pack('>%dI' % len(a), *a)


def mpi_to_int(s):
    """
    A Multi-precision integer is encoded as a series of bytes in big-endian
    order. The first two bytes are a header which tell the number of bits in
    the integer. The rest of the bytes are the integer.
    """
    return int(binascii.hexlify(s[2:]), 16)


def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modular_inverse(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def base64_url_decode(data):
    data += '=' * (4 - len(data) % 4)
    return b64decode(data.replace('-', '+').replace('_', '/'))

def base64_url_encode(data):
    return b64encode(data).decode().replace('+', '-').replace('/', '_').rstrip('=')


def base64_to_a32(s):
    return str_to_a32(base64_url_decode(s))


def a32_to_base64(a):
    return base64_url_encode(a32_to_str(a))


def get_chunks(size):
    p = 0
    s = 0x20000
    while p + s < size:
        yield (p, s)
        p += s
        if s < 0x100000:
            s += 0x20000
    yield (p, size - p)


def make_id(length):
    text = ''
    possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    for i in range(length):
        text += random.choice(possible)
    return text
