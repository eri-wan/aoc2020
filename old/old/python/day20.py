import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"

neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
                            range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]


def append_if_exists(dictionary: dict, key, val):
    if key not in dictionary.keys():
        dictionary[key] = []

    dictionary[key].append(val)


def rotate_left_90(array: np.array):
    new_array = np.array(np.flipud(array.T))
    return new_array


def rotate_right_90(array: np.array):
    new_array = np.array(np.fliplr(array.T))
    return new_array


def find_opposite_border(border_id):
    absval = abs(border_id)
    sgn = border_id/absval
    return sgn(border_id) * (((border_id + 1) % 4) + 1)


def flip_to_match_on_left(block, desired_left_border):
    flipped_block = block
    for flip in range(2):
        for rotation in range(4):
            matches = True
            for i, char in enumerate(desired_left_border):
                if char != flipped_block[i, 0]:
                    matches = False
                    break
            if matches:
                return flipped_block
            else:
                flipped_block = rotate_left_90(flipped_block)
        flipped_block = block
        flipped_block = np.flipud(flipped_block)

    raise ValueError("Couldn't find a matching orientation!")


def flip_to_match_on_top(block, desired_top_border):
    flipped_block = block.copy()
    for flip in range(2):
        for rotation in range(4):
            matches = True
            for i, char in enumerate(desired_top_border):
                if char != flipped_block[0, i]:
                    matches = False
                    break
            if matches:
                return flipped_block
            else:
                flipped_block = rotate_left_90(flipped_block)
        flipped_block = block
        flipped_block = np.flipud(flipped_block)

    raise ValueError("Couldn't find a matching orientation!")


def remove_sea_monster(whole_image: np.array, sea_monster: np.array, i, j):
    if ((whole_image[i:(i + sea_monster.shape[0]), j:(j+sea_monster.shape[1])] & sea_monster) == sea_monster).all():
        whole_image[i:(i + sea_monster.shape[0]), j:(j+sea_monster.shape[1])] = \
            whole_image[i:(i + sea_monster.shape[0]), j:(j+sea_monster.shape[1])] & np.logical_not(sea_monster)
        return True
    return False


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    blocks = {}

    count_rules = 0
    for line_block_no in range(0, len(lines), 12):
        number_line = lines[line_block_no]
        number = int(number_line[5:number_line.find(":")])
        block = []
        for line_no in range(line_block_no+1, line_block_no + 11):
            block.append([char for char in lines[line_no]])

        blocks[number] = np.array(block)

    borders_to_ids = {}
    block_to_border = {}

    for number, block in blocks.items():
        block_borders = []
        # upper border
        block_borders.append(block[0, :])
        # right border
        block_borders.append(block[:, -1])
        # lower border
        block_borders.append(block[-1, ::-1])
        # left border
        block_borders.append(block[::-1, 0])
        block_to_border[number] = {}
        for idn, border in enumerate(block_borders):
            border_id = idn + 1
            border_str = ''.join(border)
            block_to_border[number][border_id] = border_str
            append_if_exists(borders_to_ids, border_str, (number, border_id))

        for idn, border in enumerate(block_borders):
            border_id = -(idn + 1)
            border_str = ''.join(reversed(border))
            block_to_border[number][border_id] = border_str
            append_if_exists(borders_to_ids, border_str, (number, border_id))

    possible_neighbours = {}

    for border, entrylist in borders_to_ids.items():
        for entry in entrylist:
            for other_entry in entrylist:
                if entry != other_entry:
                    append_if_exists(possible_neighbours, entry[0], other_entry)

    lonesome_blocks = []
    border_blocks = []
    for tile, neighbours in possible_neighbours.items():
        if len(neighbours) <= 4:
            lonesome_blocks.append(tile)
        if len(neighbours) <= 6:
            border_blocks.append(tile)

    mult = 1
    for tile in lonesome_blocks:
        mult *= tile

    side_len = len(border_blocks) // 4 + 1

    print(f"Found {len(lonesome_blocks)} corners: {lonesome_blocks}. Mulitplication is {mult}. Side len is {side_len} ({len(blocks.keys())} blocks total)")
    # merge together blocks

    block1 = lonesome_blocks[0]
    lonesome_borders = []
    for border_id, border in block_to_border[block1].items():
        if len(borders_to_ids[border]) < 2 and border_id > 0:  # choose positive orientation
            lonesome_borders.append(border_id)

    assert len(lonesome_borders) == 2
    if lonesome_borders[0] < lonesome_borders[1] or (tuple(lonesome_borders) == (1, 4)):
        lonesome_borders = list(reversed(lonesome_borders))

    print(lonesome_borders)
    whole_image = np.full((side_len * 8, side_len * 8), False)

    block = blocks[block1]
    for rotation_times in range(abs(lonesome_borders[1]) - 1):
        block = rotate_left_90(block)

    print(block)

    whole_image[:8, :8] = block[1:-1, 1:-1] == '#'

    final_block_orientation = {}
    final_blocks = {}
    final_block_orientation[(0, 0)] = block
    final_blocks[(0, 0)] = block1

    for i in range(side_len):
        if i != 0:
            j = 0
            previous_block = final_block_orientation[(i - 1, j)]
            previous_block_id = final_blocks[(i - 1, j)]
            border_to_match = previous_block[-1, :]

            matching_borders = borders_to_ids[''.join(border_to_match)]
            next_block_id = [ident[0] for ident in matching_borders if ident[0] != previous_block_id][0]
            next_block = flip_to_match_on_top(blocks[next_block_id], border_to_match)
            final_block_orientation[(i, j)] = next_block
            final_blocks[(i, j)] = next_block_id
            whole_image[(i * 8):((i + 1) * 8), (j * 8):((j + 1) * 8)] = next_block[1:-1, 1:-1] == '#'

        for j in range(1, side_len):
            previous_block = final_block_orientation[(i, j - 1)]
            previous_block_id = final_blocks[(i, j - 1)]
            border_to_match = previous_block[:, -1]

            matching_borders = borders_to_ids[''.join(border_to_match)]
            print(matching_borders)
            print([ident[0] for ident in matching_borders if ident[0] != previous_block_id])
            next_block_id = [ident[0] for ident in matching_borders if ident[0] != previous_block_id][0]
            next_block = flip_to_match_on_left(blocks[next_block_id], border_to_match)
            final_block_orientation[(i, j)] = next_block
            final_blocks[(i, j)] = next_block_id
            whole_image[(i * 8):((i + 1) * 8), (j * 8):((j + 1) * 8)] = next_block[1:-1, 1:-1] == '#'

    print(whole_image)
    for row in whole_image:
        for col in row:
            print('#' if col else '.', end='')
        print('')

    for i in range(side_len):
        for j in range(side_len):
            print(final_blocks[(i,j)], end=' ')

        print('')


    # find sea monsters

    sea_monster_ascii = ['                  # ',
                         '#    ##    ##    ###',
                         ' #  #  #  #  #  #   ']

    sea_monster_array = np.array([[char == '#' for char in line] for line in sea_monster_ascii])

    sea_monsters = []
    new_sea_monster = sea_monster_array
    for i in range(4):
        sea_monsters.append(new_sea_monster)
        new_sea_monster = rotate_right_90(new_sea_monster)
    new_sea_monster = np.fliplr(new_sea_monster)
    for i in range(4):
        sea_monsters.append(new_sea_monster)
        new_sea_monster = rotate_right_90(new_sea_monster)

    for sea_monster in sea_monsters:
        count_sea_monsters = 0
        sea_monster_image = whole_image.copy()
        sea_monster_size = sea_monster.shape
        for i in range(sea_monster_image.shape[0] - sea_monster_size[0]):
            for j in range(sea_monster_image.shape[1] - sea_monster_size[1]):
                count_sea_monsters += remove_sea_monster(sea_monster_image, sea_monster, i, j)

        print(f"Sea monster ")
        for i in range(sea_monster_size[0]):
            for j in range(sea_monster_size[1]):
                print('#' if sea_monster[i,j] else ' ', end='')
            print('')
        print(f"was found {count_sea_monsters} time(s)")
        print(f"{np.sum(sea_monster_image)} rough waters left.")




if __name__ == "__main__":
    main()
