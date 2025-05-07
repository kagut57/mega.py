from Crypto.Cipher import AES
import json
import base64
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

def aes_cbc_encrypt(data: bytes, key: bytes) -> bytes:
    aes_cipher = AES.new(key, AES.MODE_CBC, b'\0' * 16)
    return aes_cipher.encrypt(data)


def aes_cbc_decrypt(data: bytes, key: bytes) -> bytes:
    aes_cipher = AES.new(key, AES.MODE_CBC, b'\0' * 16)
    return aes_cipher.decrypt(data)


def aes_cbc_encrypt_a32(data, key):
    return str_to_a32(aes_cbc_encrypt(a32_to_str(data), a32_to_str(key)))


def aes_cbc_decrypt_a32(data, key):
    return str_to_a32(aes_cbc_decrypt(a32_to_str(data), a32_to_str(key)))


def stringhash(s: str, aeskey):
    s32 = str_to_a32(s.encode('utf-8'))
    h32 = [0, 0, 0, 0]
    for i in range(len(s32)):
        h32[i % 4] ^= s32[i]
    for _ in range(0x4000):
        h32 = aes_cbc_encrypt_a32(h32, aeskey)
    return a32_to_base64((h32[0], h32[2]))


def prepare_key(arr):
    pkey = [0x93C467E3, 0x7DB0C7A4, 0xD1BE3F81, 0x0152CB56]
    for _ in range(0x10000):
        for j in range(0, len(arr), 4):
            key = [arr[i + j] if i + j < len(arr) else 0 for i in range(4)]
            pkey = aes_cbc_encrypt_a32(pkey, key)
    return pkey


def encrypt_key(a, key):
    return sum((aes_cbc_encrypt_a32(a[i:i + 4], key) for i in range(0, len(a), 4)), ())


def decrypt_key(a, key):
    return sum((aes_cbc_decrypt_a32(a[i:i + 4], key) for i in range(0, len(a), 4)), ())


def encrypt_attr(attr: dict, key):
    attr_str = 'MEGA' + json.dumps(attr)
    attr_bytes = attr_str.encode('utf-8')
    if len(attr_bytes) % 16:
        attr_bytes += b'\0' * (16 - len(attr_bytes) % 16)
    return aes_cbc_encrypt(attr_bytes, a32_to_str(key))


def decrypt_attr(attr: bytes, key):
    attr = aes_cbc_decrypt(attr, a32_to_str(key))
    attr = attr.rstrip(b'\0')
    if attr.startswith(b'MEGA{"'):
        return json.loads(attr[4:].decode('utf-8'))
    return False


def a32_to_str(a):
    return struct.pack(f'>{len(a)}I', *a)


def str_to_a32(b):
    if isinstance(b, str):
        b = b.encode('latin1')
    if len(b) % 4:
        b += b'\0' * (4 - len(b) % 4)
    return struct.unpack(f'>{len(b) // 4}I', b)


def mpi_to_int(s: bytes) -> int:
    return int(binascii.hexlify(s[2:]), 16)


def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_gcd(b % a, a)
        return g, x - (b // a) * y, y


def modular_inverse(a, m):
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError('modular inverse does not exist')
    return x % m


def base64_url_decode(data: str) -> bytes:
    data += '=='[(2 - len(data) * 3) % 4:]
    data = data.replace('-', '+').replace('_', '/').replace(',', '')
    return base64.b64decode(data)


def base64_to_a32(s: str):
    return str_to_a32(base64_url_decode(s))


def base64_url_encode(data: bytes) -> str:
    data = base64.b64encode(data).decode('latin1')
    return data.replace('+', '-').replace('/', '_').replace('=', '')


def a32_to_base64(a):
    return base64_url_encode(a32_to_str(a))


def get_chunks(size):
    p = 0
    s = 0x20000
    while p + s < size:
        yield p, s
        p += s
        if s < 0x100000:
            s += 0x20000
    yield p, size - p


def make_id(length):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choices(chars, k=length))
