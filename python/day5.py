import numpy as np
inputfile = "input"


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


def main():

    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line)

    print(f"Read {len(lines)} lines")

    numtrees = 0
    numfalse = 0
    countblocks = 0

    current_line = ""

    maxp = 0
    minp = np.inf

    listp = []

    for line in lines:
        lineedit = line.strip()

        lineedit = lineedit.replace("B", "1")
        lineedit = lineedit.replace("F", "0")
        lineedit = lineedit.replace("R", "1")
        lineedit = lineedit.replace("L", "0")

        number = int(lineedit, 2)
        listp.append(number)
        if number >= maxp:
            maxp=number
            print(f"New max: {number} for line {line} ({lineedit})")
        if number <= minp:
            minp= number

    listp.sort()
    for i, num in enumerate(listp[:-1]):
        if listp[i+1] != num + 1:
            print(f"Found it! {num} and next is {listp[i+1]} ")

    return


if __name__ == "__main__":
    main()
