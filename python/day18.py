import numpy as np
import re

inputfile = "input18"

alphabet = "abcdefghijklmnopqrstuvwxyz"
numbers = "1234567890"

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


def evaluate(expression_list: list):
    expression_list = expression_list + [")"]
    return evaluate_parenthesis(expression_list)


def evaluate_parenthesis(expression_list: list):
    result_sum = 0
    operator = "+"
    while len(expression_list) > 0:
        next_element = ""
        while next_element == "":
            next_element = expression_list.pop(0)
        next_number = 0

        if next_element[0] in numbers:
            next_number += int(next_element)
        elif next_element == "(":
            next_number += evaluate_parenthesis(expression_list)
        else:
            raise ValueError(f"Wrong element: {next_element}")

        if operator == "+":
            result_sum += next_number
        elif operator == "*":
            result_sum *= evaluate_plus(expression_list, next_number)
        else:
            raise ValueError(f"Wrong operator: {operator}")

        next_operator = ""
        while next_operator == "":
            next_operator = expression_list.pop(0)

        if next_operator == ")":
            return result_sum
        else:
            operator = next_operator


def evaluate_plus(expression_list: list, current_sum=0):
    while len(expression_list) > 0:
        if expression_list[0] == "":
            expression_list.pop(0)
            continue
        if expression_list[0] == "+":
            expression_list.pop(0)
            next_element = ""
            while next_element == "":
                next_element = expression_list.pop(0)
            if next_element[0] in numbers:
                current_sum += int(next_element)
            elif next_element == "(":
                current_sum += evaluate_parenthesis(expression_list)
            else:
                raise ValueError(f"Wrong element: {next_element}")
        else:
            return current_sum


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
    total_sum = 0
    for line_no, line in enumerate(lines):

        line = line.replace(")", " ) ")
        line = line.replace("(", " ( ")

        parts = line.split(" ")

        result = evaluate(parts)
        total_sum += result
        result = evaluate(parts)
        print(f"Line no {line_no:3d}: {result}")

    print(f"Total sum: {total_sum}")

if __name__ == "__main__":
    main()
