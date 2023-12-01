# import numpy as np
import re

inputfile = "input3"
example = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
'''

alphabet = "abcdefghijklmnopqrstuvwxyz"

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
    
    priorities = {}
    for number, letter in enumerate(alphabet):
        priorities[letter] = number + 1
        priorities[letter.capitalize()] = number + 27

    # score = 0
    # for line in lines:
    #     # print(line)
    #     first_half = line[:len(line)//2]
    #     second_half = line[len(line)//2:]
    #     for letter in second_half:
    #         if letter in first_half:
    #             score += priorities[letter]
    #             # print(f'{first_half} contains {letter}({priorities[letter]}) from {second_half}')
    #             break

    score = 0
    for starting_line in range(0, len(lines), 3):
        counts = {key: 0 for key in priorities.keys()}
        for line in lines[starting_line:starting_line+3]:
            present_in_line = {}
            for letter in line:
                present_in_line[letter] = True
            for key, value in present_in_line.items():
                counts[key] += 1

        for key, value in counts.items():
            if value == 3:
                score += priorities[key]
                print(f'{lines[starting_line:starting_line+3]} contain {key}')

    print(f'Sum: {score}')

    print(f"Read {len(lines)} lines")




if __name__ == "__main__":
    main()
