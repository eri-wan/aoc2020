import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"

neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
                            range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]
print(neighbouring_coordinates)


def build_start(lines):
    starting_field = set()
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == '#':
                starting_field.add((i, j, 0, 0))

    return starting_field


def update(field_set):
    count = {}
    for key in field_set:
        for neighbour in neighbouring_coordinates:
            neighbour_coordinate = tuple(key + neighbour)
            coordinate_count = count.get(neighbour_coordinate, 0)
            count[neighbour_coordinate] = coordinate_count + 1

    next_field_set = set()
    for key, value in count.items():
        if value == 3:
            next_field_set.add(key)
        elif value == 2 and key in field_set:
            next_field_set.add(key)

    return next_field_set


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    field = build_start(lines)

    print(f"Num active: {len(field)}")
    for i in range(6):
        field = update(field)
        print(f"Num active: {len(field)}")


if __name__ == "__main__":
    main()
