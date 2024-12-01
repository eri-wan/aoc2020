import re


inputfile = "input"
# example = """\
# 1abc2
# pqr3stu8vwx
# a1b2c3d4e5f
# treb7uchet"""

example = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

all_numbers = {
    "one": 1, "two":2, "three":3, "four":4, "five": 5, "six":6, "seven": 7, "eight":8, "nine": 9}
all_numbers.update({str(num):num for num in range(1,10)})


def find_frontback(pattern: str, target: str) -> tuple:
    result_front = target.find(pattern)
    if result_front == -1:
        result_front = len(target)
    
    result_back = target.rfind(pattern)
    return result_front, result_back
    
    
def find_closest(patterns: list, target: str) -> tuple:
    
    best_front_idx = len(target)
    best_front = None
    best_back_idx = -1
    best_back = None
    for pattern in patterns:
        result_front, result_back = find_frontback(pattern=pattern, target=target)
        if result_front < best_front_idx:
            best_front = pattern
            best_front_idx = result_front
        if result_back > best_back_idx:
            best_back_idx = result_back
            best_back = pattern

    assert best_back is not None
    assert best_front is not None

    return best_front, best_back



def main():
    import sys
    lines = []
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        lines = example.splitlines()
    else: 
        file_contents = ''
        with open(inputfile) as infile:
            file_contents = infile.read()
        
        lines = file_contents.splitlines()

    print(f"Read {len(lines)} lines")

    numbers = []
    for line in lines:
        best_front, best_back = find_closest(all_numbers.keys(), line)
        number_front = all_numbers[best_front]
        number_back = all_numbers[best_back]
        number = int("".join([str(number_front), str(number_back)]))
        numbers.append(number)
    
    print(numbers)
    print(f"Sum: {sum(numbers)}")

if __name__ == "__main__":
    main()
