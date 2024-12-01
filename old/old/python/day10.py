import numpy as np
import re
inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    numbers = [int(line) for line in lines]

    sorted_jolts = sorted(numbers)
    number_of_jumps = np.zeros((3), dtype=int)

    current_joltage = 0
    for number in sorted_jolts:
        diff = number - current_joltage
        if 1 <= diff <= 3:
            number_of_jumps[diff - 1] += 1
            current_joltage = number
        else:
            print(f"break in joltage between {current_joltage} and {number}!")

    number_of_jumps[2] += 1

    print(f"Number of jumps for 1-3 jolts: {number_of_jumps}, product {number_of_jumps[0] * number_of_jumps[2]}")

    sorted_jolts = [0] + sorted_jolts + [sorted_jolts[-1] + 3]

    connections_to_adapters = np.zeros(len(sorted_jolts), dtype=int)
    connections_to_adapters[0] = 1

    for i, joltage in enumerate(sorted_jolts):
        for j in range(i):
            diff = joltage - sorted_jolts[j]
            if 1 <= diff <= 3:
                connections_to_adapters[i] += connections_to_adapters[j]

    print(f"Number of connections to device: {connections_to_adapters[-1]}")


if __name__ == "__main__":
    main()
