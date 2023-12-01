import numpy as np
import re

inputfile = "input13"
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
    import sys
    lines = []
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        lines = example.splitlines()
    else: 
        file_contents = ''
        with open(inputfile) as infile:
            file_contents = infile.read()
        
        lines = file_contents.splitlines() 

    print(f"Read {len(lines)} lines")


if __name__ == "__main__":
    main()
