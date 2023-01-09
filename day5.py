# import numpy as np
import re

inputfile = "input5"
example = '''    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
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

    empty_line = lines.index('')
    num_stacks = (len(lines[0]) + 1) // 4

    stacks = {(i + 1):[] for i in range (num_stacks)}
    for stack_line in lines[:empty_line - 1]:
        for i in range(num_stacks):
            letter = stack_line[i * 4 + 1]
            if stack_line[i * 4 + 1] != ' ':
                stacks[i + 1].insert(0,letter)
    
    print(stacks)

    for line in lines[empty_line + 1:]:
        words = line.split(' ')
        move_count = int(words[1])
        move_from = int(words[3])
        move_to = int(words[5])

        moved = stacks[move_from][-move_count:]
        stacks[move_from] = stacks[move_from][:-move_count]
        # stacks[move_to] = stacks[move_to] + list(reversed(moved))
        stacks[move_to] = stacks[move_to] + moved
        print(stacks)
    
    for i in range(num_stacks):
        print(stacks[i + 1][-1], end='')
        
    print(stacks)

if __name__ == "__main__":
    main()
