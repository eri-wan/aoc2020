import numpy as np
import re

inputfile = "input8"
example = '''30373
25512
65332
33549
35390'''

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

def main():
    file_contents = ''
    with open(inputfile) as infile:
        file_contents = infile.read()
    
    lines = file_contents.splitlines()
    # lines = example.splitlines()

    print(f"Read {len(lines)} lines")

    numbers = np.array([[int(x) for x in line] for line in lines], dtype=int)
    is_visible = np.zeros_like(numbers, dtype=bool)

    print(numbers)

    # left = numbers[:-1,:]
    # right = numbers[1:,:]
    # top = numbers[:,:-1]
    # bottom = numbers[:,1:]
        
    # visible_from_left = ((right - left) > 0)[:-1, 1:-1]
    # print(visible_from_left)
    # visible_from_right = ((left - right) > 0)[1:, 1:-1]
    # visible_from_top = ((bottom - top) > 0)[1:-1, :-1]
    # visible_from_bottom = ((top - bottom) > 0)[1:-1, 1:]

    # visible_lr = np.logical_and(visible_from_left, visible_from_right)
    # visible_tb = np.logical_and(visible_from_top, visible_from_bottom)
    # visible_in_interior = np.logical_and(visible_tb, visible_lr)

    # inside_invisible = np.sum(np.logical_not(visible_in_interior))
    
    # total_visible = numbers.shape[0] * numbers.shape[1] - inside_invisible

    # print(f'total_visible: {total_visible}, inside invis: {inside_invisible}')




    for i in range(numbers.shape[0]):
        max_col = -1
        for j in range(numbers.shape[1]):
            if numbers[i,j] > max_col:
                is_visible[i,j] = True
                max_col = numbers[i,j]

        max_col = -1
        for j in range(numbers.shape[1] - 1, -1, -1):
            if numbers[i,j] > max_col:
                is_visible[i,j] = True
                max_col = numbers[i,j]
    
    for j in range(numbers.shape[1]):
        max_col = -1
        for i in range(numbers.shape[0]):
            if numbers[i,j] > max_col:
                is_visible[i,j] = True
                max_col = numbers[i,j]

        max_col = -1
        for i in range(numbers.shape[0] - 1, -1, -1):
            if numbers[i,j] > max_col:
                is_visible[i,j] = True
                max_col = numbers[i,j]
    
    # print(is_visible)

    print(np.sum(is_visible))

    max_scenic_score = 0
    for i in range(numbers.shape[0]):
        for j in range(numbers.shape[1]):
            score = calc_scenic_score(numbers, i, j)
            if score > max_scenic_score:
                max_scenic_score = score
                print(f'max scenic at ({i},{j}): {score}')

    # treecount = 0
    # for i, line in enumerate(lines):
    #     for j, x in enumerate(line):
    #         if i == 0 or i == len(lines) - 1 or j == 0 or j == len(line) - 1:
    #             continue

    #         is_visible = False
    #         for neighbour in neighbours:
    #             if lines[i + neighbour[0]][j + neighbour[1]] < x:
    #                 is_visible = True
    #                 break
    #         if is_visible:
    #             print(f'tree ({i}, {j}): {x} is visible')
    #             treecount += 1

    # left
    

    # print(treecount)



if __name__ == "__main__":
    main()
