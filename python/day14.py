import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


def generate_addresses(address:int, mask:str):
    floating = [0xFFFFFFFFF]
    for i, char in enumerate(reversed(mask)):
        if char == 'X':
            val = 2 ** i
            add_floats = []
            for floater in floating:
                add_floats.append(floater ^ val)

            floating += add_floats

    number_mask = int(mask.replace('X', '1'), 2)
    result = []
    for floater in floating:
        result.append((address | number_mask) & floater)

    return result



def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    mask_ones = 0
    mask_zeroes = 0xFFFFFFFF
    values1 = {}

    # lines = ["mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X", "mem[8] = 11", "mem[7] = 101", "mem[8] = 0"]

    for line in lines:
        if "]" in line:
            begin_bracket = line.find('[')
            end_bracket = line.find(']')
            address = int(line[(begin_bracket + 1): end_bracket])
            value = int(line[end_bracket + 4:])
            values1[address] = (value & mask_zeroes) | mask_ones
        else:
            number = line[7:]
            mask_ones = int(number.replace('X', '0'), 2)
            mask_zeroes = int(number.replace('X', '1'), 2)

    print(f"Sum of values is memory is {sum(values1.values())}")

    mask = "0" * 36
    values2 = {}

    # lines = ["mask = 000000000000000000000000000000X1001X", "mem[42] = 100","mask = 00000000000000000000000000000000X0XX","mem[26] = 1"]

    # print(lines)
    tally = 0

    for line in lines:
        if "]" in line:
            begin_bracket = line.find('[')
            end_bracket = line.find(']')
            address = int(line[(begin_bracket + 1): end_bracket])
            value = int(line[end_bracket + 4:])
            addresses = generate_addresses(address, mask)
            # print(f"generated addresses: {addresses}")
            print(f"num addresses: {len(addresses)}, min: {min(addresses)}, max: {max(addresses)}, diff: {max(addresses) - min(addresses)}, mask len {len(mask)}")
            for gen_address in addresses:
                if gen_address in values2.keys():
                    tally -= values2[gen_address]
                values2[gen_address] = value
                tally += value
        else:
            number = line[7:]
            mask = number

    print(f"Sum of values is memory is {sum(values2.values())}, comp: {tally}")



if __name__ == "__main__":
    main()
