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

def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line)

    print(f"Read {len(lines)} lines")

    countblocks = 0
    countgroups = 0

    current_line = ""
    thisset = set()

    count = 0

    rules = {}

    for line in lines:
        countblocks += 1
        if line != "\n":
            thisline = make_rule(line)
            print(thisline)
            rules.update(thisline)
        else:
            raise ValueError

    inverted = {}

    for key in rules.keys():
        inverted[key] = []

    for key, value in rules.items():
        for color, count in value:
            inverted[color].append((key, count))

    num_parents = 0
    find_parents_of = ['shiny gold']
    have_discovered = set()
    while len(find_parents_of) > 0:
        next_parent = find_parents_of.pop(0)
        for parent in inverted[next_parent]:
            if parent[0] not in have_discovered:
                have_discovered.add(parent[0])
                find_parents_of.append(parent[0])
                num_parents += 1

    num_children = 0
    find_children_of = ['shiny gold']

    calculated = {}

    def find_num_children(key: str):
        if key not in calculated:
            count = 0
            for child, countchildren in rules[key]:
                count += countchildren * (1 + find_num_children(child))
            calculated[key] = count

        return calculated[key]



    have_discovered = set()
    while len(find_children_of) > 0:
        next_parent = find_children_of.pop(0)
        for parent in inverted[next_parent]:
            if parent[0] not in have_discovered:
                have_discovered.add(parent[0])
                find_children_of.append(parent[0])
                num_children += 1


    # if len(current_set) != 0:
    #     countgroups += 1
    #     thiscount = len(thisset)
    #     count += thiscount
    #     print(f"current_line: {thiscount} : {thisset}")

    print(f"In total {len(rules)} rules, {countblocks} colors, {num_parents} colors can hold your bag, {find_num_children('shiny gold')} bags in your bag..")


if __name__ == "__main__":
    main()
