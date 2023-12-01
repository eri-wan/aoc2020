
inputfile = "input"


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line)

    course = (1, 2)
    numtrees = 0
    numemptries = 0
    for i in range(0, len(lines), course[1]):
        line = lines[i].strip()
        linewidth = len(line)

        if line[i // course[1] * course[0] % linewidth] == '#':
            numtrees += 1
        else:
            if line[i // course[1] * course[0] % linewidth] != '.':
                print("ERROR! got " + line[i // course[1] * course[0] % linewidth])
            numemptries += 1

    print("Num trees: {}, num empties: {}, num lines: {}".format(numtrees, numemptries, len(lines)))

    return


if __name__ == "__main__":
    main()
