import numpy as np
import functools

inputfile = "input16"
example = '''>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'''
ROCKS_TEXT=['####',
    '''.#.
    ###
    .#.'''
    ,'''..#
    ..#
    ###''',
    '''#
    #
    #
    #'''
    '''##
    ##'''
    ,
]


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

def rock_overlap(rock_candidate, stage, depth):
    pass

def push_rock(rock, stage, rock_coordinate, jet):
    if (jet == -1 and rock_coordinate[1] == 0) or (jet == +1 and rock_coordinate[1] + rock.shape[1] == 7):
        return rock_coordinate
    
    rock_bottom = max(rock_coordinate[0], -1)
    rock_top = max(rock_coordinate[0] - rock.shape[0], -1)

    for line_index, overlapping_line in enumerate(stage[-rock_bottom:-rock_top]):
        pass
        

def propagate_rock(rock, stage, jet_pattern, jet_counter):
    rock_coordinate = (-4, 2)
    
    finished = False
    while not finished:
        jet = jet_pattern[jet_counter]
        jet_counter = (jet_counter + 1) % len(jet_counter)
        rock_coordinate = push_rock(rock, stage, rock_coordinate, jet)
        finished, rock_coordinate = fall_rock(rock, stage, rock_coordinate)
    set_rock(rock, stage, rock_coordinate)
    return jet_counter



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


    jet_pattern = np.array([+1 if letter == '>' else -1 for letter in lines[0]])
    rocks = [
        np.array([[True if letter == '#' else False for letter in line] for line in rock.splitlines()], dtype=bool) for rock in ROCKS_TEXT
    ]

    stage = [[True for i in range(9)], [True if i == 0 or i == 8 else False for i in range(9)]]
    
    rock_counter = 0
    jet_counter = 0
    while rock_counter < 11:
        rock = rocks[rock_counter % 5]


        jet_counter = propagate_rock(rock, stage, jet_pattern, jet_counter)

        rock_counter += 1
        print(f'after {rock_counter} rocks:')
        print(stage)




if __name__ == "__main__":
    main()
