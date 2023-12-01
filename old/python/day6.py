import numpy as np
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


def countl(line):
    dictl = {}
    for char in line:
        dictl[char] = True

    return len(dictl)


def toset(line):
    thisset = set()
    for char in line:
        thisset.add(char)

    return thisset


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

    for line in lines:
        countblocks += 1
        if line != "\n":
            current_set = toset(line)
            if len(thisset) == 0:
                thisset = current_set
            else:
                thisset.intersection_update(current_set)
            print(thisset)

        else:
            thisset.remove('\n')
            countgroups += 1
            thiscount = len(thisset)
            count += thiscount
            print(f"current_line: {thiscount} : {thisset}")
            thisset = set()

    if len(current_set) != 0:
        countgroups += 1
        thiscount = len(thisset)
        count += thiscount
        print(f"current_line: {thiscount} : {thisset}")

    print(f"In total {count} yeses, from {countgroups} groups with {countblocks} people.")


if __name__ == "__main__":
    main()
