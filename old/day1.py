# import numpy as np
import re

inputfile = "input1"

alphabet = "abcdefghijklmnopqrstuvwxyz"

# neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
#                             range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]


def append_if_exists(dictionary: dict, key, val):
    if key not in dictionary.keys():
        dictionary[key] = []

    dictionary[key].append(val)

def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())
    
    print(f"Read {len(lines)} lines")

    best_sums = [0, 0, 0]
    current_sum = 0
    for line in lines:
        if line == '':
            if current_sum > best_sums[0]:
                best_sums = sorted(best_sums + [current_sum])[1:]
                print(f"new best sum: {best_sums}")
            current_sum = 0
        else:
            current_sum += int(line)

    if current_sum > best_sums[0]:
        best_sums = sorted(best_sums + [current_sum])[1:]
        print(f"new best sum: {best_sums}, sum: {sum(best_sums)}")

    print(f"best sum: {best_sums}")
    



if __name__ == "__main__":
    main()
