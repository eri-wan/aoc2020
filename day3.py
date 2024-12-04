import sys


test_input = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"""

def read_input(input: str) -> str:
    return input

def main():
    input = None
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        with open(input_filename, 'r') as file:
           input = file.read()
    else:
           input = test_input
 
    string = read_input(input)
    
    ## part 1

    def is_number(string: str) -> bool:
        for char in string:
            if char not in "0123456789":
                return False
        return True

    total_sum = 0
    candidates = string.split("mul(")
    for candidate in candidates:
        end_mul = candidate.find(")")
        if end_mul == -1:
            continue
        number_candidates = candidate[:end_mul].split(",")
        if len(number_candidates) == 2 and is_number(number_candidates[0]) and is_number(number_candidates[1]):
            # print(f"{candidate} matches")
            total_sum += int(number_candidates[0]) * int(number_candidates[1])
        else:
            # print(f"{candidate} does not match") 
            pass    
        
         
    print(total_sum)

    ## part 2
    sum_part_2 = 0
    index_do = 0
    while index_do >= 0 and index_do < len(string):
        index_dont = string.find("don't()", index_do) # don't() is never found in do(), so ignore offsetting index
            
        # print(f"do->don't: {string[index_do:(index_dont+5) if index_dont > 0 else -1]}")

        candidates = string[index_do:index_dont].split("mul(")[1:]  # skip first until "mul("
        for candidate in candidates:
            end_mul = candidate.find(")")
            if end_mul == -1:
                continue
            number_candidates = candidate[:end_mul].split(",")
            if len(number_candidates) == 2 and is_number(number_candidates[0]) and is_number(number_candidates[1]):
                print(f"{candidate} matches")
                sum_part_2 += int(number_candidates[0]) * int(number_candidates[1])
            else:
                print(f"{candidate} does not match")
        
        index_do = string.find("do()", index_dont)  # do() is never found in don't(), so ignore offsetting index
            
        
         
    print(sum_part_2)

    # print(count_total)



            
        

         
        

    


if __name__ == "__main__":
    main()
