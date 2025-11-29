import sys
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
from Crypto.Random.random import getrandbits
print("p?")
p = int(input(), 16)
print("g?")
g = int(input(), 16)
print("A?")
A = int(input(), 16)

b = getrandbits(2048)
B = pow(g, b, p)
print(f"B = {B:#x}\n")

s = pow(A, b, p)
# print(f"s = {s:#x}\n")

key = s.to_bytes(256, "little")[:16]
print(key)

cipher = AES.new(key, mode = AES.MODE_CBC)

# key_hex = input()
print("input flag cipher hex")
flag_cipher_hex = input()

# cipher = AES.new(bytes.fromhex(key_hex), mode=AES.MODE_ECB)
print(cipher.decrypt(bytes.fromhex(flag_cipher_hex)))