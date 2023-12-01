import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


class FerryState:

    cardinal_directions = {
        "E": np.array((1, 0)),
        "N": np.array((0, 1)),
        "S": np.array((0, -1)),
        "W": np.array((-1, 0)),
    }
    rotations = {
        "L": np.array(((0, -1), (1, 0))),
        "R": np.array(((0, 1), (-1, 0)))
    }

    def __init__(self):
        self.direction = np.array((1, 0), dtype=int)
        self.coordinate = np.array((0, 0), dtype=int)

        self.waypoint_coord = np.array((0, 0), dtype=int)

    def take_instruction(self, instruction_line: str):
        instruction = instruction_line[0]
        count = int(instruction_line[1:])

        if instruction in self.cardinal_directions.keys():
            self.coordinate += self.cardinal_directions[instruction] * count
        elif instruction in self.rotations.keys():
            times = count // 90
            for i in range(times):
                self.direction = self.rotations[instruction].dot(self.direction)
        elif instruction == "F":
            self.coordinate += self.direction * count
        else:
            raise ValueError(f'Cannot understand instruction "{instruction_line}"')

    def __str__(self):
        return f"Coordinate: {self.coordinate} | Direction: {self.direction}"


class FerryAndWaypointState:

    cardinal_directions = {
        "E": np.array((1, 0)),
        "N": np.array((0, 1)),
        "S": np.array((0, -1)),
        "W": np.array((-1, 0)),
    }
    rotations = {
        "L": np.array(((0, -1), (1, 0))),
        "R": np.array(((0, 1), (-1, 0)))
    }

    def __init__(self):
        self.coordinate = np.array((0, 0), dtype=int)
        self.waypoint_rel_coord = np.array((10, 1), dtype=int)

    def take_instruction(self, instruction_line: str):
        instruction = instruction_line[0]
        count = int(instruction_line[1:])

        if instruction in self.cardinal_directions.keys():
            self.waypoint_rel_coord += self.cardinal_directions[instruction] * count
        elif instruction in self.rotations.keys():
            times = count // 90
            for i in range(times):
                self.waypoint_rel_coord = self.rotations[instruction].dot(self.waypoint_rel_coord)
        elif instruction == "F":
            self.coordinate += self.waypoint_rel_coord * count
        else:
            raise ValueError(f'Cannot understand instruction "{instruction_line}"')

    def __str__(self):
        return f"Coordinate: {self.coordinate} | Waypoint: {self.waypoint_rel_coord}"


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    ferry = FerryState()
    print(f"Ferry: {ferry}")
    for count, line in enumerate(lines):
        ferry.take_instruction(line)
        print(f"{count:3} : {line} : Ferry now at {ferry}")
    print(f"Ferry ended up at {sum(abs(ferry.coordinate))} Manhattan distance from start")

    ferry = FerryAndWaypointState()
    print(f"Ferry: {ferry}")
    for count, line in enumerate(lines):
        ferry.take_instruction(line)
        print(f"{count:3} : {line} : Ferry now at {ferry}")
    print(f"Ferry ended up at {sum(abs(ferry.coordinate))} Manhattan distance from start")

if __name__ == "__main__":
    main()
