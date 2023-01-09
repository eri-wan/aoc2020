# import numpy as np
import re

totsum = []

inputfile = "input7"
example = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = alphabet.capitalize()

# neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
#                             range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]


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

    tree = {}
    current = tree

    for line in lines[1:]:
        # print(line)
        if line == "$ ls":
            continue
        elif line[:5] == '$ cd ':
            dirname = line[5:].strip()
            if dirname == '..':
                current = current['..']
            elif dirname == '/':
                current = tree
            else:
                current = current[dirname]
        elif line[:4] == 'dir ':
            dirname = line[4:]
            current[dirname] = {
                '..': current
            }
        else:
            size, name = line.split(' ')
            current[name] = int(size)
    
    bigsum = 70000000
    needed = 30000000
    totsize = traverse(tree)
    free_space = (bigsum - totsize)
    need_to_free = needed - free_space

    free_size = 0
    sorted_dirlist = sorted(totsum)
    for entry in sorted_dirlist:
        if entry > need_to_free:
            free_size = entry
            break


    print(f'total sum: {totsize}, free_space{free_space}, need to free {need_to_free}, delete sum of dirs {free_size} ')

if __name__ == "__main__":
    main()
