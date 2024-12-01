import numpy as np
import re
inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"


def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    numbers = [int(line) for line in lines]

    moving_window_size = 25

    def test_against_window(target_number, window):
        assert len(window) == moving_window_size
        for i in range(moving_window_size):
            for j in range(i + 1, moving_window_size):
                if window[i] + window[j] == target_number:
                    return True
        return False

    current_num = 0

    for number_index in range(moving_window_size, len(numbers)):
        current_num = numbers[number_index]
        if not test_against_window(current_num, numbers[number_index - moving_window_size:number_index]):
            print(f"{current_num} is not the sum of any two of {numbers[number_index - moving_window_size:number_index]}")
            break

    assert current_num == 507622668
    target_num = current_num

    for number_index, number in enumerate(numbers):
        number_sum = 0
        sum_index = number_index
        while number_sum < target_num and sum_index < len(numbers):
            number_sum += numbers[sum_index]
            sum_index += 1
        if number_sum == target_num:
            sublist = sorted(numbers[number_index:sum_index-1])
            maxnum = max(sublist)
            minnum = min(sublist)
            print(f"Found range from {number_index}:{numbers[number_index]} to {sum_index-1}:{numbers[sum_index-1]} summing to {target_num}. Min {minnum} and max {maxnum} sum to {maxnum + minnum}. ({numbers[number_index:sum_index]})")
            break


if __name__ == "__main__":
    main()
