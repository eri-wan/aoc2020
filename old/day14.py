import numpy as np
import re

inputfile = "input14"
example = '''498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9'''

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

sand_directions = [np.array(coord) for coord in [(0, 1), (-1, 1), (1, 1)]]
def move_sand(sand_coord, map):
    for direction in sand_directions:
        test_coord = tuple(sand_coord + direction)
        if min(test_coord) < 0 or min(np.array(map.shape) - test_coord) <= 0 or not map[test_coord]:
            return test_coord
    return None


def main():
    file_contents = ''
    with open(inputfile) as infile:
        file_contents = infile.read()
    
    lines = file_contents.splitlines() 
    # lines = example.splitlines()

    print(f"Read {len(lines)} lines")

    walls = []
    sand_start = (500,0)
    corner_lu = sand_start
    corner_br = sand_start

    for line in lines:
        wall = []
        parts = line.split(' -> ')
        for part in parts:
            x_text, y_text = part.split(',')
            coord = (int(x_text), int(y_text))
            corner_lu = tuple(min(lu, c) for lu, c in zip(corner_lu, coord))
            corner_br = tuple(max(lu, c) for lu, c in zip(corner_br, coord))
            wall.append(coord)
    
        walls.append(wall)

    # shift to accomodate for floor
    floor_level = corner_br[1] + 2
    floor_left = min(sand_start[0] - (floor_level + 5), corner_lu[0])
    floor_right = max(sand_start[0] + (floor_level + 5), corner_br[0])
    corner_lu = (floor_left, corner_lu[1])
    corner_br = (floor_right, floor_level)
    walls.append([(floor_left, floor_level), (floor_right, floor_level)])

    cave_size = (np.array(corner_br) - corner_lu) + (1, 1)
    cave_map = np.zeros(cave_size, dtype=bool)

    # let's shift the coords
    walls = [[tuple(coord - np.array(corner_lu)) for coord in wall] for wall in walls]
    sand_start = tuple(sand_start - np.array(corner_lu))
    corner_br = tuple(corner_br - np.array(corner_lu))

    for wall in walls:
        corner1 = wall[0]
        cave_map[corner1] = True
        
        for corner2 in wall[1:]:
            diff = corner2 - np.array(corner1)
            dist = np.max(np.abs(diff))
            direction = np.clip(corner2 - np.array(corner1), -1, 1)

            for i in range(dist):
                cave_map[tuple(corner1 + direction * (i+1))] = True

            corner1 = corner2

    sand_count = 0
    finished = False
    while not finished:
        sand = sand_start
        sand_stopped = False
        while not sand_stopped:
            # move sand
            new_coord = move_sand(sand, cave_map)
            if new_coord is None:
                sand_stopped = True
                cave_map[sand] = True
                sand_count += 1
                break
            elif min(new_coord) < 0 or min(np.array(cave_map.shape) - new_coord) <= 0:
                finished = True
                break
            sand = new_coord
        if sand == sand_start:
            finished = True
            print('sand full!')

    print(f'Got {sand_count} sands')
    print(cave_map.T)
        
        
                









if __name__ == "__main__":
    main()
