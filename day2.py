# import numpy as np
import re

inputfile = "input2"

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
    
    print(f"Read {len(lines)} lines")

    # lines = ["A Y", "B X", "C Z"]


    order = {'A': 0, 'B': 1, 'C': 2, 'X': 0, 'Y': 1, 'Z': 2, }
    value = {'A': 0, 'B': 0, 'C': 0, 'X': 1, 'Y': 2, 'Z': 3, }
    scores = {
        ('A', 'X') : 0,
        ('B', 'X') : 0,
        ('C', 'X') : 0,
        ('A', 'Y') : 0,
        ('B', 'Y') : 0,
        ('C', 'Y') : 0,
        ('A', 'Z') : 0,
        ('B', 'Z') : 0,
        ('C', 'Z') : 0,
    }
    for key in scores.keys():
        # winning_score = ((order[key[1]] - order[key[0]] + 1) % 3) * 3 
        # scores[key] += winning_score + value[key[1]]
        losedrawwin = order[key[1]] - 1
        selected_choice_score = ((order[key[0]] + losedrawwin) % 3) + 1
        scores[key] += selected_choice_score + order[key[1]] * 3

    print(f'scores dict: {scores}')

    tuples = []
    for line in lines:
        tuples.append(tuple(line.split(' ')))
    
    tot_score = 0
    for line in tuples:
        print (scores[line])
        tot_score += scores[line]

    print(f'total score: {tot_score}')


if __name__ == "__main__":
    main()
