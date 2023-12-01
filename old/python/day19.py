import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"

neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
                            range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]


def remove_rule_conforming(rules: dict, next_rule_s: list, remaining: str):

    print(f"Checking rule {next_rule_s} with input {remaining}")

    if len(next_rule_s) == 0 or len(remaining) == 0:
        return len(next_rule_s) == 0 and len(remaining) == 0

    first_rule = rules[next_rule_s[0]]

    if isinstance(first_rule, str):
        if remaining[0] == first_rule:
            return remove_rule_conforming(rules, next_rule_s[1:], remaining[1:])
        else:
            return False
    elif isinstance(first_rule, int):
        next_rule_s = [rules[first_rule]] + next_rule_s[1:]
        return remove_rule_conforming(rules, next_rule_s, remaining)
    elif isinstance(first_rule, list):
        next_rule_s = first_rule + next_rule_s[1:]
        return remove_rule_conforming(rules, next_rule_s, remaining)
    elif isinstance(first_rule, tuple):
        for or_rule in first_rule:
            remaining_after_rule = remaining

            evaluate_next = or_rule + next_rule_s[1:]
            if remove_rule_conforming(rules, evaluate_next, remaining_after_rule):
                return True
            else:
                continue

    return False


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

    count_rules = 0
    for line in lines:
        if line == "":
            break
        count_rules += 1

        parts = line.split(": ")
        rule_no = int(parts[0])
        if "\"" in line:
            rules[rule_no] = parts[1][1]
            continue

        or_rules = parts[1].split(" | ")
        rule_lists = []
        for rule in or_rules:
            rule_lists.append([int(rule_number) for rule_number in rule.split(" ")])
        rules[rule_no] = tuple(rule_lists)

    print(rules)

    matching_rules = 0
    for line in lines[count_rules + 1:]:
        if remove_rule_conforming(rules, [0], line):
            print(f"Confirming line {line}!")
            matching_rules += 1

    print(f"Number of matching rules: {matching_rules}")


if __name__ == "__main__":
    main()
