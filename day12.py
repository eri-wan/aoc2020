import numpy as np
import re

inputfile = "input12"
example = '''Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi'''

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = alphabet.capitalize()

neighbours = [(1, 0), (0, 1), (-1, 0), (0, -1)]

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

def test(level, divisor):
    return level % divisor == 0

def can_visit(coord, visited):
    return np.all(np.greater_equal(coord, np.zeros_like(coord))) and np.all(np.less(coord,visited.shape)) and not visited[coord]

def main():
    file_contents = ''
    with open(inputfile) as infile:
        file_contents = infile.read()
    
    lines = file_contents.splitlines() 
    # lines = example.splitlines()

    print(f"Read {len(lines)} lines")

    numbers = np.array(
        [
            [
                ord(char) for char in line    
            ]    for line in lines
        ]
    , dtype=int)
    start = ord('S')
    end = ord('E')

    print(np.argwhere(numbers == start)[0])
    start_coord = tuple(np.argwhere(numbers == start)[0])
    end_coord = tuple(np.argwhere(numbers == end)[0])

    numbers[start_coord] = ord('a')
    numbers[end_coord] = ord('z')
    rows = numbers.shape[0]
    cols = numbers.shape[1]

    print(numbers)

    visited = np.zeros_like(numbers, dtype=bool)
    visited[end_coord] = True
    search_next = [end_coord]

    # print(visited[(start_coord[0] - 2):(start_coord[0] + 5), (start_coord[1]):(start_coord[1] + 5)])
    # print(search_next)

    steps = 0
    found = False
    while search_next:
        steps += 1
        search_next_round = []
        # print(search_next)
        for visitee in search_next:
            if found:
                break
            for direction in neighbours:
                neighbour = tuple(visitee + np.array(direction))
                if can_visit(neighbour, visited) and numbers[visitee] - numbers[neighbour] <= 1:
                    if numbers[neighbour] == ord('a'):
                        search_next_round = []
                        found = True
                        print(f'found end!!! in {steps} steps at {neighbour} (from ({visitee})\n{numbers[neighbour]}->{numbers[visitee]}')
                        break
                    # print(neighbour)
                    search_next_round.append(neighbour)
                    visited[neighbour] = True
        search_next = search_next_round

    print(f'Found road from {start_coord} to {end_coord} in {steps} steps')

    print(start, end)


if __name__ == "__main__":
    main()
