import sys


test_input = """3   4
4   3
2   5
1   3
3   9
3   3"""

def read_input(input: str) -> list[list[int]]:
    return [[int(entry) for entry in line.split()] for line in input.split('\n') if line]

def main():
    input = None
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        with open(input_filename, 'r') as file:
            input = file.read()
    else:
            input = test_input

    rows = read_input(input)
    
    list_left = []
    list_right = []
    for row in rows:
        print(row)
        list_left.append(row[0])
        list_right.append(row[1])

    ## part 1
    # sorted_left = sorted(list_left)
    # sorted_right = sorted(list_right)

    # total_sum = sum(abs(left - right) for left, right in zip(sorted_left, sorted_right))

    # print(f"total sum: {total_sum}")

    ## part 2
    sum_total = sum(value_left * sum(value_left == value_right for value_right in list_right) for value_left in list_left)
    print(sum_total)
        

    


if __name__ == "__main__":
    main()
