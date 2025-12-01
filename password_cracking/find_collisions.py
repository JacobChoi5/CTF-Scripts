import sys
user_hash_path = sys.argv[1]
pass_hash_path = sys.argv[2]

uhf = open(user_hash_path)
phf = open(pass_hash_path)

phdict = {}

for line in phf:
    line = line.strip()
    ph = line.split(': ')
    phdict[ph[1]] = ph[0]

updict = {}

for line in uhf:
    line = line.strip()
    up = line.split(': ')
    if up[1] in phdict:
        updict[up[0]] = phdict[up[1]]

cracker = open("cracked.txt", 'w')

for key in sorted(updict.keys()):
    # print(f"{key}: {updict[key]}")
    cracker.write(f"{key}: {updict[key]}\n")