# import numpy as np
import re

inputfile = "input4"
example = '''2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
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

    print(f"Read {len(lines)} lines")

    counts = 0

    for line in lines:
        words = line.split(',')
        # pairs = []
        # rev_pairs = []
        # for pair in words:
        #     pairs.append(tuple(int(x) for x in pair.split('-')))
        #     rev_pairs.append(tuple(reversed(pairs[-1])))
        
        begins = []
        ends = []
        for word in words:
            thesplit = word.split('-')
            begins.append(int(thesplit[0]))
            ends.append(int(thesplit[1]))

        # def check_first_contained_in_second(begins_, ends_):
        #     return begins_[0] <= begins_[1] and ends_[0] >= ends_[1]
        # contains = check_first_contained_in_second(begins, ends) or check_first_contained_in_second(list(reversed(begins)), list(reversed(ends)))
        
        def check_first_overlap_in_second(begins_, ends_):
            return not(begins_[0] > ends_[1] or ends_[0] < begins_[1])
        
        contains = check_first_overlap_in_second(begins, ends) # or check_first_overlap_in_second(list(reversed(begins)), list(reversed(ends)))
        print(f'{words} containment is {contains}')
        counts += contains

    print(f"{counts} contained other")





if __name__ == "__main__":
    main()
