import sys

test_input = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

def parse_input(input: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    first_part, second_part = input.split('\n\n')  # should only be two parts
    before_after = [tuple(int(entry) for entry in row.split('|') if entry) for row in first_part.split("\n") if row]
    prompts = [[int(entry) for entry in row.split(",")] for row in second_part.split("\n") if row]
    assert all(len(edge) == 2 for edge in before_after)
    return before_after, prompts

def topological_sort(all_orderings: list[tuple[int, int]]):
    starting_pages = set(before for before, _ in all_orderings if before not in [after for _, after in all_orderings])
    if not starting_pages:  # Needs to be at least one page coming before all others
        return []

    sorted_list = []
    while starting_pages:
        page = starting_pages.pop()
        sorted_list.append(page)

        after_pages: list[int] = [after for before, after in all_orderings if before == page]
        for after_page in after_pages:
            all_orderings.remove((page, after_page))
            if after_page not in [after for _, after in all_orderings]:
                # page no longer has any other pages before it so it can be inserted now
                starting_pages.add(after_page)

    if all_orderings:  # Some dependencies are unfulfillable
        return []
    
    return sorted_list


def find_all_after(entry: int, before_after: list[tuple[int, int]], visited: set[int] | None=None) -> set[int]:
    if visited is None:
        visited = set()

    to_visit = set([after for before, after in before_after if before == entry and after not in visited])
    while to_visit:
        entry_to_visit = to_visit.pop()
        visited.add(entry_to_visit)
        to_visit |= set([after for before, after in before_after if before == entry_to_visit and after not in visited])
    
    return visited




def main():
    input = None
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
        with open(input_filename, 'r') as file:
           input = file.read()
    else:
           input = test_input
 
    before_after, prompts = parse_input(input)

    accepted_lines = []
    # part 1
    total_sum = 0

    for line in prompts:
        visited = None
        found_inconsistencies = False
        # print(f"Visiting line : {line}")
        for entry in reversed(line):
            visited= find_all_after(entry, [(before, after) for before, after in before_after if before in line and after in line], visited)
            # print(f"Found: {visited}")
            if entry in visited:
                found_inconsistencies = True
                break

        if not found_inconsistencies:
            total_sum += line[len(line) // 2]
            accepted_lines.append(line)
    
    print(total_sum)

    ## part 2
    total_sum = 0
    for line in prompts:
        if line in accepted_lines:
            continue

        sorted_line = topological_sort([(before, after) for before, after in before_after if before in line and after in line])
        assert sorted_line
        # print(sorted_line)
        total_sum += sorted_line[len(line) // 2]

        

    print(total_sum)



            
        

         
        

    


if __name__ == "__main__":
    main()
