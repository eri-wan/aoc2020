import copy
import sys

test_input = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""


def read_input(input: str) -> list[list[str]]:
    return [
        list(char for char in string.strip()) for string in input.split("\n") if string
    ]


def main():
    input = None
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        with open(input_filename, "r") as file:
            input = file.read()
    else:
        input = test_input

    input_map = read_input(input)
    size = (len(input_map), len(input_map[0]))

    assert all(len(row) == len(input_map[0]) for row in input_map)

    def within_range(coordinate: tuple[int, int]) -> bool:
        return all(value >= 0 and value < size[i] for i, value in enumerate(coordinate))

    def get_element_at(map: list[list[str]], coord: tuple[int, int]) -> str:
        return map[coord[0]][coord[1]]

    ## part 1
    map_of_visited = [[False for char in row] for row in input_map]
    pos_of_guard = [
        (row_index, col_index)
        for row_index, row in enumerate(input_map)
        for col_index, value in enumerate(row)
        if value == "^"
    ][0]
    direction_of_guard = (-1, 0)
    guard_90_deg_turn_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    guard_directions_after_turn = guard_90_deg_turn_directions[1:] + [
        guard_90_deg_turn_directions[0]
    ]
    direction_to_next = {
        current: next
        for current, next in zip(
            guard_90_deg_turn_directions, guard_directions_after_turn
        )
    }
    while True:
        map_of_visited[pos_of_guard[0]][pos_of_guard[1]] = True
        next_pos = tuple(pos_of_guard[i] + direction_of_guard[i] for i in range(2))

        if not within_range(next_pos):
            break

        if input_map[next_pos[0]][next_pos[1]] == "#":
            direction_of_guard = direction_to_next[direction_of_guard]
            # print(f"Turned at {pos_of_guard} to face {direction_of_guard}")
        else:
            pos_of_guard = next_pos

    found = sum(elem for row in map_of_visited for elem in row)

    print(found)

    ## part 2
    loops_found = 0
    previous_directions_at_coord: dict[tuple[int, int], list[tuple[int, int]]] = {}
    pos_of_guard = [
        (row_index, col_index)
        for row_index, row in enumerate(input_map)
        for col_index, value in enumerate(row)
        if value == "^"
    ][0]
    direction_of_guard = (-1, 0)

    def will_guard_loop(
        current_pos: tuple[int, int],
        current_dir: tuple[int, int],
        map_to_check: list[list[str]],
    ) -> tuple[bool, list[tuple[tuple[int, int], tuple[int, int]]]]:
        directions_visited_at_coord: dict[tuple[int, int], list[tuple[int, int]]] = {}
        pos_and_directions_visited_in_order: list[
            tuple[tuple[int, int], tuple[int, int]]
        ] = []
        guard_90_deg_turn_directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        guard_directions_after_turn = guard_90_deg_turn_directions[1:] + [
            guard_90_deg_turn_directions[0]
        ]
        direction_to_next = {
            current: next
            for current, next in zip(
                guard_90_deg_turn_directions, guard_directions_after_turn
            )
        }
        while True:
            pos_and_directions_visited_in_order.append((current_pos, current_dir))

            if current_dir in directions_visited_at_coord.get(
                current_pos, list()
            ):  # detected a loop!
                # print(
                #     f"Loop detected! Pos {current_pos}, dir {current_dir}\nvisited:{pos_and_directions_visited_in_order}"
                # )
                return True, pos_and_directions_visited_in_order

            directions_visited_at_coord.setdefault(current_pos, []).append(current_dir)
            next_pos: tuple[int, int] = tuple(
                current_pos[i] + current_dir[i] for i in range(2)
            )

            if not within_range(next_pos):
                return False, pos_and_directions_visited_in_order

            if map_to_check[next_pos[0]][next_pos[1]] == "#":
                current_dir = direction_to_next[current_dir]
                # print(f"Turned at {current_pos} to face {current_dir}")
            else:
                current_pos = next_pos

    did_base_scenario_loop, base_scenario_visited_pos_and_directions = will_guard_loop(
        pos_of_guard, direction_of_guard, input_map
    )
    assert not did_base_scenario_loop
    assert (
        len(set(pos for pos, dir in base_scenario_visited_pos_and_directions)) == found
    )

    map_of_tried = [[False for _ in row] for row in input_map]

    for position, direction in base_scenario_visited_pos_and_directions:
        next_pos: tuple[int, int] = tuple(position[i] + direction[i] for i in range(2))
        if (
            within_range(next_pos)
            and next_pos != pos_of_guard
            and input_map[next_pos[0]][next_pos[1]] != "#"
            and not map_of_tried[next_pos[0]][next_pos[1]]
        ):
            map_of_tried[next_pos[0]][next_pos[1]] = True
            modified_map = copy.deepcopy(input_map)
            modified_map[next_pos[0]][next_pos[1]] = "#"
            is_looping, _ = will_guard_loop(position, direction, modified_map)
            if is_looping:
                # print(f"Loop found placing '#' at {next_pos}")
                loops_found += 1

    print(loops_found)

if __name__ == "__main__":
    main()
