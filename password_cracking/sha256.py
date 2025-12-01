import sys
import hashlib

filepath = sys.argv[1]
f = open(filepath)

pass_dict = {}

filename = filepath[:-4] + "sha256" + ".txt"

for line in f:
    line = line.strip()
    hasher = hashlib.sha256()
    hasher.update(line.encode())
    pass_dict[line] = hasher.hexdigest()

wf = open(filename, 'w')

for key in sorted(pass_dict):
    wf.write(f"{key}: {pass_dict[key]}\n")