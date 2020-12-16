import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


def check_against_rules_any(value, rules):
    for rule_name, rules_values in rules.items():
        if rules_values[0][0] <= value <= rules_values[0][1] or rules_values[1][0] <= value <= rules_values[1][1]:
            return True
    return False

def check_against_rules_line(values, rules, possible_cols):
    for rule_name, rules_values in rules.items():
        for col in possible_cols[rule_name].copy():
            if not (rules_values[0][0] <= values[col] <= rules_values[0][1] or rules_values[1][0] <= values[col] <= rules_values[1][1]):
                possible_cols[rule_name].remove(col)


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    your_ticket_index = lines.index("your ticket:")
    my_values = [int(value) for value in lines[your_ticket_index + 1].split(",")]

    rules = {}

    for rule_line in lines[:your_ticket_index -1]:
        colon = rule_line.find(":")
        name = rule_line[:colon]
        pairs = rule_line[colon + 2:].split(" or ")
        pair1 = tuple(int(value) for value in pairs[0].split("-"))
        pair2 = tuple(int(value) for value in pairs[1].split("-"))
        rules[name] = (pair1, pair2)

    invalid_lines = []
    invalid_values = []
    valid_lines = []
    for line_num, ticket_line in enumerate(lines[your_ticket_index + 4:]):
        values = [int(value) for value in ticket_line.split(",")]
        for value in values:
            if not check_against_rules_any(value, rules):
                invalid_lines.append(line_num)
                invalid_values.append(value)

    for line_num, ticket_line in enumerate(lines[your_ticket_index + 4:]):
        values = [int(value) for value in ticket_line.split(",")]
        if line_num not in invalid_lines:
            valid_lines.append(values)

    possible_cols = {}
    for key in rules.keys():
        possible_cols[key] = [i for i in range(len(my_values))]

    finished_rules = {}

    for line_num, ticket_line in enumerate(valid_lines):

        check_against_rules_line(ticket_line, rules, possible_cols)
        finished = [None]
        while len(finished) > 0:
            if finished[0] is not None:
                for rule_name in finished:
                    rules.pop(rule_name)
                    possible_cols.pop(rule_name)
            finished = []

            for rule_name, only_possible_cols in possible_cols.items():
                if len(only_possible_cols) < 2:
                    assert len(only_possible_cols) == 1
                    definitely_column_number = only_possible_cols[0]
                    finished_rules[rule_name] = definitely_column_number
                    finished.append(rule_name)
                    for other_rule in rules.keys():
                        if rule_name != other_rule and definitely_column_number in possible_cols[other_rule]:
                            possible_cols[other_rule].remove(definitely_column_number)




    mult = 1
    count = 0
    for rule_name in finished_rules.keys():
        if "departure" in rule_name:
            mult *= my_values[finished_rules[rule_name]]
            count += 1

    print(f"Sum of invalid values is {sum(invalid_values)}, num: {len(invalid_values)}")

    print(f"Columns used: {finished_rules}")

    print(f"Finished multiplication of \"departure\" fields value: {mult}, (fields count {count})")






if __name__ == "__main__":
    main()
