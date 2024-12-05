import sys
from tracemalloc import start


test_input = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""

def read_input(input: str) -> list[list[str]]:
    return [list(char for char in string.strip()) for string in input.split('\n') if string]

def main():
    input = None
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        with open(input_filename, 'r') as file:
           input = file.read()
    else:
           input = test_input
 
    inputs = read_input(input)
    size = (len(inputs), len(inputs[0]))

    assert all(len(row) == len(inputs[0]) for row in inputs)

    def within_range(coordinate: tuple[int, int]) -> bool:
        return all(value >= 0 and value < size[i] for i, value in enumerate(coordinate))

    
    ## part 1
    xmas_list = ["X", "M", "A", "S"]
    letter_to_next = {xmas_list[i]: (xmas_list[i+1] if i+1 < len(xmas_list) else None) for i in range(len(xmas_list))}
    starting_coordinates = [(row, col) for row, input_row in enumerate(inputs) for col, letter in enumerate(input_row) if letter == xmas_list[0]]

    found = 0
    ## search. Not proud of this one; I read the question wrong and didn't see that they had to be in a line, so I implemented BFS/DFS for XMAS. Ugly. 
    to_visit = [(starting_coordinate, None) for starting_coordinate in starting_coordinates]
    while to_visit:
        (current_row, current_col), current_dir = to_visit.pop()
        next_letter = letter_to_next[inputs[current_row][current_col]]
        if current_dir is not None:
            next_coordinate_and_dirs = [((current_row + current_dir[0], current_col + current_dir[1]), current_dir)]
        else:
            next_coordinate_and_dirs = [((current_row + delta_row, current_col + delta_col), (delta_row, delta_col)) for delta_row in [-1, 0, 1] for delta_col in [-1, 0, 1]]
        next_coordinate_and_dirs = [next_coordinate_and_dir for next_coordinate_and_dir in next_coordinate_and_dirs if within_range(next_coordinate_and_dir[0]) and inputs[next_coordinate_and_dir[0][0]][next_coordinate_and_dir[0][1]] == next_letter]
        if next_letter == xmas_list[-1] and len(next_coordinate_and_dirs) > 0:
            found += len(next_coordinate_and_dirs)
            starting_coordinate = tuple(value - current_dir[i] * 2 for i, value in enumerate([current_row, current_col]))
            assert inputs[starting_coordinate[0]][starting_coordinate[1]] == "X"
            # print(f"start: {current_row - current_dir[0] * 2, current_col - current_dir[1] * 2}, Current: {current_row, current_col}, dir: {current_dir}, next letter: {next_letter}, next_coordinates: {next_coordinate_and_dirs}, found: {found}, to_visit: {to_visit}")
        else:
            to_visit += next_coordinate_and_dirs

    print(found)

    ## part 2
    starting_coordinates = [(row, col) for row, input_row in enumerate(inputs) for col, letter in enumerate(input_row) if letter == "A"]
    directions= [(1,1), (1,-1), (-1,-1), (-1,1)] # in the right order
    to_find = ["M", "M", "S", "S"]

    found = 0
    ## search
    for row, col in starting_coordinates:
        for direction_permutation in range(len(directions)):
            current_dirs = [directions[(i + direction_permutation) % 4] for i in range(len(directions))]  # permute either answer or dirs
            is_wrong = False
            for direction, expected_letter in zip(current_dirs, to_find):
                row_dir, col_dir = direction
                next_row = row + row_dir
                next_col = col + col_dir
                if not within_range((next_row, next_col)) or inputs[next_row][next_col] != expected_letter:
                    is_wrong = True
                    break
            if not is_wrong:
                found += 1
                # print(f"row:{row}, col:{col}")
                break

    print(found)



            
        

         
        

    


if __name__ == "__main__":
    main()
