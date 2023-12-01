import numpy as np
import re
inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


tags = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]  # "cid"
eycols = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def build_pass_dict(line: str):
    result_dict = {}
    for entry in line.split():
        colon = line.find(':')
        if colon == -1:
            print(f"weird entry: {entry}")
        key = line[:colon]
        value = line[colon+1:]
        result_dict[key] = value
    return result_dict


def validate(line):
    print(line)
    try:
        for tag in tags:
            offs = line.find(tag)
            if offs != -1:
                space = line.find(" ", offs + 3)

                substr = line[offs + 4:space]

                if tag == "byr":
                    yr = int(substr)
                    if not (yr <= 2002 and yr >= 1920):
                        return False

                if tag == "iyr":
                    yr = int(substr)
                    if not 2010 <= yr <= 2020:
                        return False
                if tag == "eyr":
                    yr = int(substr)
                    if not 2020 <= yr <= 2030:
                        return False
                if tag == "hgt":
                    if not (substr[2:] == "in" and 59 <= int(substr[:2]) <= 76):
                        if not (substr[3:] == "cm" and 150 <= int(substr[:3]) <= 193):
                            return False
                if tag == "hcl":
                    if len(substr) == 7 and substr[0] == '#':
                        int(substr[1:], 16)
                        continue
                    return False
                if tag == "ecl":
                    if substr not in eycols:
                        return False
                if tag == "pid":
                    if not (len(substr) == 9 and int(substr) >= 0):
                        return False
            else:
                return False

    except ValueError:
        return False

    return True


def toset(line):
    thisset = set()
    for char in line:
        thisset.add(char)

    return thisset


def make_rule(line: str):
    color = line[:line.find(" bag")]
    contains = line.find("contain ")
    bags = line[contains + 8:]

    children = []

    if bags != "no other bags.\n":
        parts = re.split(r" bags?[\,\.]? ?", bags)
        for part in parts:
            if len(part) > 6:
                space = part.find(' ')
                number = int(part[0:space])
                key = part[space + 1:]
                children.append((key, number))

    return {color: children}


def visit(line, accumulator):
    nop = 0
    if line[:3] == "jmp":
        return int(line[4:]), accumulator, nop
    if line[:3] == "acc":
        accumulator += int(line[4:])
    if line[:3] == "nop":
        nop = int(line[4:])
    return 1, accumulator, nop

def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    rules = {}

    # for line in lines:
    #     if line != "\n":
    #         thisline = make_rule(line)
    #         print(thisline)
    #         rules.update(thisline)
    #     else:
    #         raise ValueError

    pc = 0
    accumulator = 0

    visited = np.zeros((len(lines)), dtype=bool)

    def go_down_the_path(now_pc, now_accumulator, now_visited):
        while 0 <= now_pc < len(lines) and not visited[now_pc]:
            now_visited[now_pc] = True
            increment, now_accumulator, _ = visit(lines[now_pc], now_accumulator)
            now_pc += increment
            assert 0 <= now_pc < len(lines)

    while not visited[pc]:
        visited[pc] = True
        increment, accumulator, _ = visit(lines[pc], accumulator)
        pc += increment
        assert 0 <= pc < len(lines)

    print(f"In total {sum(visited)} steps, accumulator was {accumulator} ")

    discovered_backwards = np.zeros((len(lines)), dtype=bool)

    sources = [[] for line in lines]
    goals = []
    for counter, line in enumerate(lines):
        jump, accumulator, nop = visit(line, 0)
        if counter + jump == len(lines):
            goals.append(counter)
        elif 0 <= counter + jump < len(lines):
            sources[counter + jump].append(counter)
        else:
            print(f"Out of range: {counter} to {counter + jump} ({line})")

    print(f"Goals: {goals}")
    to_visit_backwards = goals
    while len(to_visit_backwards) > 0:
        to_visit_next = to_visit_backwards.pop(0)
        for source in sources[to_visit_next]:
            if not discovered_backwards[source]:
                to_visit_backwards.append(source)
                discovered_backwards[source] = True


    print(sum(discovered_backwards))

    pc = 0
    accumulator = 0
    visited_x_2 = np.zeros((len(lines)), dtype=bool)

    done = False

    while not visited_x_2[pc]:
        visited_x_2[pc] = True
        increment, accumulator, nop = visit(lines[pc], accumulator)

        if not done and nop != 0:
            if discovered_backwards[pc + nop]:
                print(f"Found it! At {pc}, jump to {pc + nop} ({lines[pc]})")
                increment = nop
                nop = 0
                done = True
        elif not done and increment != 1:
            if discovered_backwards[pc + 1]:
                print(f"Found it! At {pc}, jump to {pc + 1} ({lines[pc]})")
                nop = increment
                increment = 1
                done = True

        pc += increment
        if pc == len(lines):
            print(f"Finished! at accumulator {accumulator}, visited {sum(visited_x_2)} nodes")
            break






if __name__ == "__main__":
    main()
