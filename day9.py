import numpy as np
import re

inputfile = "input9"
example = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''

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
    # lines = example.splitlines()

    visited_points = set()
    starting_point = (0,0)
    rope = [np.array((0,0)) for i in range(10)]
    current_head = np.array((0,0))
    current_tail = np.array((0,0))
    visited_points.add(tuple(current_tail))
    
    for line in lines:
        parts = line.split(' ')
        dir = np.array(directions[parts[0]])
        times = int(parts[1])

        # print(line)
        for i in range(times):
            rope[0], rope[1] = move_rope(rope[0], rope[1], dir)
            for rope_link in range(1,len(rope)-1):
                rope[rope_link], rope[rope_link+1] = move_rope(rope[rope_link], rope[rope_link+1], (0,0))
            visited_points.add(tuple(rope[-1]))
            # print(f'Move: {dir}, current rope: {rope}')

    print (visited_points, len(visited_points))

    print(f"Read {len(lines)} lines")


if __name__ == "__main__":
    main()
