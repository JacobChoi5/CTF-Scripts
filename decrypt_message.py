from Crypto.Util.strxor import strxor

lines = [
    "00 0d 1a 07 26 3a 37 6b 11 1c 3a 07 39 0b 15 46 06 02 1a 4c 00 3c 10 43 07 17 04 25 4c 03 09 10 00",
    "0d 0d 19 53 06 74 33 2a 0b 59 3b 16 31 01 52 1f 0a 16 54 1c 1c 21 03 06 16 06 09 38 4c 00 04 15 1f",
    "15 1f 0c 00 20 39 35 6b 0a 17 2c 53 24 0c 1f 03 45 13 15 08 59 3a 16 43 02 1d 17 2a 05 19 06 59 53",
    "0d 09 10 53 38 31 70 3f 04 15 22 53 31 07 1d 13 11 43 00 04 1c 73 04 0d 06 05 00 33 1f 57 0f 16 04",
    "1d 48 01 1c 3f 31 70 25 0a 59 3a 07 25 01 17 08 11 43 17 0d 17 73 17 06 14 16 45 35 04 1e 12 59 53",
    "00 00 08 07 6f 23 3f 3e 09 1d 69 11 35 45 03 13 0c 17 11 4c 1c 3e 07 02 07 00 04 32 1f 1e 0f 1e 53",
    "18 1d 0a 18 26 38 29 6b 2a 2d 19 53 39 16 52 16 00 11 12 09 1a 27 09 1a 55 01 00 22 1e 12 15 59 53",
    "03 09 1a 1d 3b 74 24 23 00 0b 2c 53 31 45 11 07 11 00 1c 4c 16 21 45 10 1a 1f 00 35 04 1e 0f 1e 53",
    "19 09 10 11 2a 74 29 2e 11 59 00 53 34 0c 16 08 11 43 04 0d 00 73 04 17 01 17 0b 35 05 18 0f 59 53",
    "03 0d 49 00 27 3b 25 27 01 59 3b 16 31 09 1e 1f 45 0f 11 0d 0b 3d 45 02 17 1d 10 35 4c 1e 15 59 53",
    "1a 09 01 53 2b 3b 3e 3f 45 0d 21 1a 3e 0e 52 11 00 43 1a 09 1c 37 45 17 1a 52 45 61 4c 57 41 59 53",
]

formatted_lines = []

# formatting lines as [["00", "0d", ...], ["0d", "0d", ...], ...]
for line in lines:
    chars = line.split(" ")
    formatted_lines.append(chars)

spaces = {}

for i in range(len(lines)): # for every sentence
    for k in range(0, 33): # for every character of that sentence
        flag = True
        for j in range(0, len(lines)): # compare to every character from every other string at same index (all are same length)
            byte_val = strxor(bytes.fromhex(lines[i]), bytes.fromhex(lines[j]))[k] # xored value of just this character

            """
            i[k] is a space: if j[k] is a lower case charater, xor result will be an upper
            ik is space: if jk is upper case, xor result will be lower
            if both are space: result is 0

            i[k] is a lowercase letter: if j[k] is a space, result will be uppercase
            ik is uppercase, if jk is space, result will be lowercase

            ik is any tpye of letter, and jk is any type of letter, result is essentiall random
            """

            if not ((65 <= byte_val <= 90) or (97 <= byte_val <= 122) or byte_val == 0): # if value of xor is not a lower/uppercase letter or 0
                # essentially, marking if it confirms that lines[i][k] IS NOT a space
                flag = False
        if flag: # if character is space, add string --> index to dict of spaces 
            if str(i) not in spaces:
                spaces[str(i)] = [k]
            else:
                spaces[str(i)].append(k)

# printing all information of EVERY SPACE, this is technically not necessary but is VERY helpful in visualizing it for me
for line_index in spaces: # for every line found with a space (all of them)
    line = formatted_lines[int(line_index)] # getting the line, this stuff is only necessary if there was a sentence without a space
    for value in spaces[line_index]: # for char expected to be a space
        print("String: " + line_index + "\tIndex: " + str(value) + "\tHex:" + line[int(value)] + "\tASCII: " + chr(int(line[int(value)], 16)))


key = {}

# taking the index of spaces and saving the encrypted or original key value at these indexes
for line_index in spaces:
    line = formatted_lines[int(line_index)]
    for i in range(len(spaces[line_index])): # for every space in this line
        val = hex(int(line[int(spaces[line_index][i])], 16) ^ 32)[2:] # !!! this xors all the encrypted spaces to reverse engineer and find the original value (ie flip from lower/upper)
        # val = hex(int(line[int(spaces[line_index][i])], 16))[2:] # this version is if you DO NOT want to xor with 32 to find the key value
        key.setdefault(spaces[line_index][i], []).append(val) # adds to key dict

key_sorted = dict(sorted(key.items())) # sorts by the index (key)
print()
print(key_sorted)
key_ascii = {k: list(map(lambda x: chr(int(x, 16)), v)) for k, v in key_sorted.items()} # converts the raw ascii values to chars
print(key_ascii)


# building cipher string by finding most common value at each index. this is NOT necessary, you can pick any random / first one
# this is to defend against false positives, which there were NONE of
from collections import Counter
cipher_string = ""
cipher_hexes = []
for i in range(33):
    if i in key_ascii:
        chars = key_ascii[i]
        char_counter = Counter(chars)
        most_common = char_counter.most_common(1) 
        cipher_string += str(most_common[0][0])
    else:
        cipher_string += "_"

print("\nCipher String:")
print(cipher_string) # this is all of the CONFIRMED values of the key

cipher_string_guess = "ThisOTPKeyIsPerfectlySecureAlways" # filling in the blanks of the key

cipher_hex = []

for char in cipher_string_guess: # converting key back to hex to xor with all the original strings
    cipher_hex.append(hex(ord(char.encode()))[2:])
    print(hex(ord(char.encode()))[2:], end=" ")

cipher_hexes = "54 68 69 73 4f 54 50 4b 65 79 49 73 50 65 72 66 65 63 74 6c 79 53 65 63 75 72 65 41 6c 77 61 79 73" # just copy pasted output lol, you can definitely automate this

print()

# strxor for each string with key and printing
for i in range(len(lines)):
    byte_val = strxor(bytes.fromhex(lines[i]), bytes.fromhex(cipher_hexes)) 
    print(byte_val.decode())