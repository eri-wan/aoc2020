import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"

def generate_next(history_dict: dict, incoming_number: int, current_index: int) -> int:
    if incoming_number in history_dict.keys():
        outgoing_start = history_dict[incoming_number]
    else:
        outgoing_start = current_index

    history_dict[incoming_number] = current_index

    return current_index - outgoing_start


def main():
    # lines = []
    # with open(inputfile) as infile:
    #     while True:
    #         line = infile.readline()
    #         if not line:
    #             break
    #         lines.append(line.strip())
    #
    # print(f"Read {len(lines)} lines")
    #
    # mask_ones = 0
    # mask_zeroes = 0xFFFFFFFF
    # values1 = {}

    seed_numbers = [1, 0, 18, 10, 19, 6]
    # seed_numbers = [3,1,2]

    history_dict = {}
    current_index = 1
    for seed_number in seed_numbers:
        next_number = generate_next(history_dict, seed_number, current_index)
        assert next_number == 0

        current_index += 1

    while current_index < 30000000:
        next_number = generate_next(history_dict, next_number, current_index)
        current_index += 1

    print(f"The {current_index}th number is {next_number}")


if __name__ == "__main__":
    main()
