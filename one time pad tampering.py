#!/usr/bin/env python3
# print("One-Time Pad Key (hex): ", end='')
# string1 = input()
# print("Flag Ciphertext (hex): ", end='')
# string2 = input()
# string1 = "d51b3c5ba0"
string1 = input()[6:]
string2 = "sleep".encode().hex()
hex1 = []
hex2 = []
# print(string1)
# print(string2)
# print(hex1)
# print(hex2)
for char in string1:
    hex1.append(int(char, 16))
for char in string2:
    hex2.append(int(char, 16))
# print(string1)
# print(string2)
# print(hex1)
# print(hex2)
decrypt = ""
for i in range(len(hex1)):
    decrypt += hex(hex1[i] ^ hex2[i])[2:]
# print(decrypt)
string3 = "flag!".encode().hex()
hex3 = []
hex4 = []
for char in string3:
    hex3.append(int(char, 16))
for char in decrypt:
    hex4.append(int(char, 16))
flag_getter = ""
for i in range(len(hex3)):
    flag_getter += hex(hex3[i] ^ hex4[i])[2:]
print("TASK: " + flag_getter)