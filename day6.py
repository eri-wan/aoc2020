# import numpy as np
import re

inputfile = "input6"
example = '''mjqjpqmgbljsphdztnvjfqwrcgsmlb
'''

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = alphabet.capitalize()

# neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
#                             range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]


def append_if_exists(dictionary: dict, key, val):
    if key not in dictionary.keys():
        dictionary[key] = []

    dictionary[key].append(val)

def main():
    file_contents = ''
    with open(inputfile) as infile:
        file_contents = infile.read()
    
    lines = file_contents.splitlines()
    # lines = example.splitlines()

    print(f"Read {len(lines)} lines")

    line = lines[0]
    for i, char in enumerate(line):
        if i < 13:
            continue
        past_chars = line[(i - 13):(i+1)]
        sorted_chars = sorted(past_chars)
        found_double = False
        for j, char in enumerate(sorted_chars[:-1]):
            if sorted_chars[j+1] == char:
                found_double = True
                break
        if found_double == False:
            print(f"Found {past_chars} after {i+1}")
            break
        

if __name__ == "__main__":
    main()
