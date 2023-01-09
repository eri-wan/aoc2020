import numpy as np
import re

inputfile = "input10"
example = '''noop
addx 3
addx -5'''
other_example = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = alphabet.capitalize()

neighbours = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def calc_scenic_score(numbers, i_tree, j_tree):
    up = 0
    down = 0
    left = 0
    right = 0

    for i in range(i_tree - 1, -1, -1):
        up += 1
        if numbers[i_tree,j_tree] <= numbers[i, j_tree]:
            break

    for i in range(i_tree + 1, numbers.shape[0], 1):
        down += 1
        if numbers[i_tree,j_tree] <= numbers[i, j_tree]:
            break

    for j in range(j_tree - 1, -1, -1):
        left += 1
        if numbers[i_tree,j_tree] <= numbers[i_tree, j]:
            break

    for j in range(j_tree + 1,  numbers.shape[1], 1):
        right += 1
        if numbers[i_tree,j_tree] <= numbers[i_tree, j]:
            break

    return up * left * down * right

def textgrid_to_numbers(lines):
    return np.array([[int(x) for x in line] for line in lines], dtype=int)

def traverse(root):
    sum = 0
    for entry in root.keys():
        if entry == '..':
            continue
        if isinstance(root[entry], dict):
            sum += traverse(root[entry])
        else:
            sum += root[entry]
    global totsum
    totsum.append(sum)
    return sum


def append_if_exists(dictionary: dict, key, val):
    if key not in dictionary.keys():
        dictionary[key] = []

    dictionary[key].append(val)

directions = {
    'R' : (0,1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)

}

def move_rope(head, tail, dir):
    new_head = head + dir
    new_diff = new_head - tail
    if any(np.abs(new_diff) > 1):
        tail_movement = np.clip(new_diff, -1, 1)
    else:
        tail_movement = 0
    new_tail = tail + tail_movement
    return new_head, new_tail

def main():
    file_contents = ''
    with open(inputfile) as infile:
        file_contents = infile.read()
    
    lines = file_contents.splitlines() 
    # lines = other_example.splitlines()

    print(f"Read {len(lines)} lines")

    i = 0
    counter = 0
    instructions = []
    register = 1
    signal_strengths = []
    image = []
    while i < len(lines) or instructions:
        if abs(counter % 40 - register) <= 1:
            image.append('#')
        else:
            image.append('.')
            
        if not instructions:
            if lines[i][:4] == 'addx':
                add = int(lines[i].split(' ')[-1])
                instructions.append([2, add])
                i += 1
            elif lines[i] == 'noop':
                i += 1
        counter += 1
        if counter % 40 == 20:
            print(f'Counter: {counter}, Register: {register}')
            signal_strengths.append(counter * register)

        if instructions:
            instructions[0][0] -= 1
            if instructions[0][0] == 0:
                register += instructions[0][1]
                instructions = instructions[1:]

    print(f'sum: {sum(signal_strengths)}, Signal strengths: {signal_strengths}')
    for line_i in range(len(image) // 40):
        print(''.join(image[line_i* 40:line_i * 40 + 40]))


if __name__ == "__main__":
    main()
