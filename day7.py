import sys

test_input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""


def parse_input(input_string: str) -> list[tuple[int, tuple[int, ...]]]:
    lines = []
    for line in input_string.split("\n"):
        if not line:
            continue
        first_part, last_part = line.split(":")
        numbers = tuple(
            int(number_string) for number_string in last_part.strip().split(" ")
        )
        lines.append((int(first_part), numbers))

    return lines


def main():
    input = None
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        with open(input_filename, "r") as file:
            input = file.read()
    else:
        input = test_input

    lines = parse_input(input)

    # part 1
    total_sum = 0
    for expected_sum, numbers in lines:
        # print(f"line: {expected_sum, numbers}")
        sum_and_numbers_left = {(numbers[0], numbers[1:])}
        possible_sums = []
        while sum_and_numbers_left:
            previous_sum, numbers_left = sum_and_numbers_left.pop()
            for operator in (
                "+",
                "*",
            ):
                if operator == "+":
                    sum_so_far = previous_sum + numbers_left[0]
                elif operator == "*":
                    sum_so_far = previous_sum * numbers_left[0]

                if len(numbers_left) == 1:
                    possible_sums.append(sum_so_far)
                    # print(f"appending {possible_sums}")
                else:
                    sum_and_numbers_left.add((sum_so_far, numbers_left[1:]))
                    # print(f"continuing with {sum_so_far, sum_and_numbers_left}")

        if expected_sum in possible_sums:
            total_sum += expected_sum

    print(total_sum)

    ## part 2
    total_sum = 0

    total_sum = 0
    for expected_sum, numbers in lines:
        # print(f"line: {expected_sum, numbers}")
        sum_and_numbers_left = {(numbers[0], numbers[1:])}
        possible_sums = []
        while sum_and_numbers_left:
            previous_sum, numbers_left = sum_and_numbers_left.pop()
            for operator in "+", "*", "||":
                if operator == "+":
                    sum_so_far = previous_sum + numbers_left[0]
                elif operator == "*":
                    sum_so_far = previous_sum * numbers_left[0]
                elif operator == "||":
                    sum_so_far = int(f"{previous_sum}{numbers_left[0]}")

                if len(numbers_left) == 1:
                    possible_sums.append(sum_so_far)
                    # print(f"appending {possible_sums}")
                else:
                    sum_and_numbers_left.add((sum_so_far, numbers_left[1:]))
                    # print(f"continuing with {sum_so_far, sum_and_numbers_left}")

        if expected_sum in possible_sums:
            total_sum += expected_sum

    print(total_sum)


if __name__ == "__main__":
    main()
