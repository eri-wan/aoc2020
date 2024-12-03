from itertools import count
import sys


test_input = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9

"""

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
    
    count_total = 0
    ## part 1
    for row in rows:
        diffs = [(right - left) for left, right in zip(row[:-1], row[1:])]
        count_total += int(all(1 <= abs(diff) <= 3 for diff in diffs) and all (diffs[0] * diff > 0 for diff in diffs[1:]))
        # print(list(diffs[0] * diff > 0 for diff in diffs[1:]))
        # print(f"count: {count_total}")
         
    print(count_total)

    count_total = 0
    for row in rows:
        diffs = [(right - left) for left, right in zip(row[:-1], row[1:])]
        safe = all(1 <= abs(diff) <= 3 for diff in diffs) and all(diffs[0] * diff > 0 for diff in diffs[1:])
        # print(f"already safe? {safe}")
        if not safe:
            for i in range(len(row)):
                smaller_row = row[:i] + row[i+1:]
                smaller_diffs = [(right - left) for left, right in zip(smaller_row[:-1], smaller_row[1:])]
                safe = all(1 <= abs(diff) <= 3 for diff in smaller_diffs) and all(smaller_diffs[0] * diff > 0 for diff in smaller_diffs[1:])
                # print(f"safe: {safe} for i={i}")
                if safe:
                    # print(f"smaller diffs: {smaller_diffs}")
                    break
        
        count_total += int(safe)


    print(count_total)



            
        

         
        

    


if __name__ == "__main__":
    main()
