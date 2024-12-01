import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


def count_occupied_neighbours(array_field, coordinate):
    a = (array_field[(coordinate[0] - 1):(coordinate[0] + 2),
         (coordinate[1] - 1):(coordinate[1] + 2)] == 1)
    return np.sum(a)

directions = np.array([(1,1), (0,1), (-1,1), (1,0), (0,-1), (1,-1), (-1,0), (-1,-1)])


def count_visible_occupied(array_field, coordinate):
    def check_direction(direction):
        current_coordinate = np.array((coordinate[0], coordinate[1]))
        current_coordinate += direction
        while np.logical_and(current_coordinate > 0, current_coordinate < array_field.shape).all():
            if array_field[current_coordinate[0], current_coordinate[1]] == 1:
                return True
            elif array_field[current_coordinate[0], current_coordinate[1]] == 0:
                break
            current_coordinate += direction

        return False

    num_occupied = 0
    for i in range(8):
        num_occupied += check_direction(directions[i, :])

    return num_occupied


def update(field: np.array):
    updated_field = field.copy()

    for i in range(1, field.shape[0] - 1):
        for j in range(1, field.shape[1] - 1):
            if field[i, j] == 0 and count_occupied_neighbours(field, (i, j)) == 0:
                updated_field[i, j] = 1
            elif field[i, j] == 1 and count_occupied_neighbours(field, (i, j)) > 4:  # 4 neighbours + self -> 5
                updated_field[i, j] = 0

    return updated_field


def update_visibility(field: np.array):
    updated_field = field.copy()

    for i in range(1, field.shape[0] - 1):
        for j in range(1, field.shape[1] - 1):
            if field[i, j] == 0 and count_visible_occupied(field, (i, j)) == 0:
                updated_field[i, j] = 1
            elif field[i, j] == 1 and count_visible_occupied(field, (i, j)) >= 5:
                updated_field[i, j] = 0

    return updated_field


def to_numpy_array(string_field):
    array_build = []
    for line in string_field:
        this_line = []
        for char in line:
            if char == '.':
                this_line.append(-1)
            elif char == 'L':
                this_line.append(0)
            elif char == '#':
                this_line.append(1)
            else:
                raise ValueError
        array_build.append(this_line)

    return np.array(array_build, dtype=int)


def count_occupied(array_field):
    return np.sum(array_field[:] == 1)


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    row_width = len(lines[0])

    empty_ghost_row = "." * row_width

    lines = [empty_ghost_row] + lines + [empty_ghost_row]

    whole_field = to_numpy_array(["." + line + "." for line in lines])

    previous_fields = [whole_field]

    iterations = 0
    found = False

    while not found:
        iterations += 1
        whole_field = update(whole_field)
        for old_field in previous_fields:
            if np.equal(whole_field, old_field).all():
                print(f"Found cycle after {iterations} iterations. it has {count_occupied(whole_field)} occupied seats.")
                found = True
                break

        previous_fields.append(whole_field)

    iterations = 0
    found = False
    whole_field = previous_fields[0]
    previous_fields = [whole_field]
    while not found:
        iterations += 1
        whole_field = update_visibility(whole_field)
        for old_field in previous_fields:
            if np.equal(whole_field, old_field).all():
                print(f"Found cycle after {iterations} iterations. it has {count_occupied(whole_field)} occupied seats.")
                found = True
                break

        previous_fields.append(whole_field)


if __name__ == "__main__":
    main()
