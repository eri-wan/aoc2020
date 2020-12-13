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

    current_ts = int(lines[0])
    frequencies = [int(entry) for entry in lines[1].split(',') if entry != 'x']

    # all are in sync with 0, so a timestamp where event occurs divides evenly with frequency
    current_min = np.inf
    min_frequency = -1

    for freq in frequencies:
        past_one = (current_ts - 1) // freq
        next_ts = (past_one + 1) * freq
        diff = next_ts - current_ts
        if diff < current_min:
            current_min = diff
            min_frequency = freq

    print(f"Best is {min_frequency} arriving in {current_min}. Product is {current_min * min_frequency}")

    offsets = {int(entry): count for count, entry in enumerate(lines[1].split(',')) if entry != 'x'}

    # find ts such that ts + offset % freq == 0 for all
    # all are primes so can just multiply to get scd


    found = False
    frequencies_sorted = np.array(sorted(frequencies, reverse=True))
    print(frequencies_sorted)
    wanted_offsets = np.array([offsets[entry] for entry in frequencies_sorted])
    print(wanted_offsets)
    cycle_frequency = 1
    cycle_offset = 1 - offsets[frequencies_sorted[0]]
    for numbers_included in range(1, len(frequencies_sorted) + 1):
        multiplier = 0
        found = False

        use_numbers = frequencies_sorted[:numbers_included]
        use_offsets = wanted_offsets[:numbers_included]
        while not found:
            target = multiplier * cycle_frequency + cycle_offset
            check = np.alltrue(np.remainder(target + use_offsets, use_numbers) == 0)
            if check:
                found = True
                print(f"found ts = {target} (multiplier {multiplier} )")
                print(f"using {use_numbers} with offsets {use_offsets}")

                cycle_frequency *= frequencies_sorted[numbers_included - 1]
                cycle_offset = target
            multiplier += 1


if __name__ == "__main__":
    main()
