import numpy as np
import re

inputfile = "input11"
example = '''Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1'''

alphabet = "abcdefghijklmnopqrstuvwxyz"
ALPHABET = alphabet.capitalize()

neighbours = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def textgrid_to_numbers(lines):
    return np.array([[int(x) for x in line] for line in lines], dtype=int)

def traverse(root):
    sum = 0
    for entry in root.keys():
        if entry == '..':
            continue
        if isinstance(root[entry], dict):
            sum += traverse(root[entry])
        else:
            sum += root[entry]
    global totsum
    totsum.append(sum)
    return sum

def append_if_exists(dictionary: dict, key, val):
    if key not in dictionary.keys():
        dictionary[key] = []

    dictionary[key].append(val)

def test(level, divisor):
    return level % divisor == 0

def main():
    file_contents = ''
    with open(inputfile) as infile:
        file_contents = infile.read()
    
    lines = file_contents.splitlines() 
    # lines = example.splitlines()

    monkeys = []

    print(f"Read {len(lines)} lines")

    common_divisor = 1

    current_monkey = {}
    monkey_number = -1
    i = 0
    while i < len(lines):
        line = lines[i]
        assert line[:6] == "Monkey"
        monkey_number = int(line.split(' ')[-1][:-1])  # remove ":"
        assert len(monkeys) == monkey_number
        current_monkey['items'] = [int(item) for item in (lines[i+1].split(': ')[1]).split(', ')]
        op_text = lines[i+2].split('new = ')[1]
        if 'old +' in op_text:
            plus = int(op_text.split(' ')[-1])
            def plus_fun(plus_):
                return lambda level: level + plus_
            current_monkey['operation'] = plus_fun(plus)
        elif 'old * old' in op_text:
            current_monkey['operation'] = lambda level: level * level
        elif 'old * ' in op_text:
            mult = int(op_text.split(' ')[-1])
            def mult_fun(mult_):
                return lambda level: level * mult_
            current_monkey['operation'] = mult_fun(mult)
        else:
            raise Exception('parsing error in op')

        current_monkey['test_div'] = int(lines[i + 3].split(' ')[-1])
        common_divisor *= current_monkey['test_div']
        current_monkey['test_res_true'] = int(lines[i + 4].split(' ')[-1])
        current_monkey['test_res_false'] = int(lines[i + 5].split(' ')[-1])
        current_monkey['activity'] = 0

        monkeys.append(current_monkey)
        current_monkey = {}

        i += 7

    # play game
    for i in range(10000):
        print(f'round {i}')
        for j, monkey in enumerate(monkeys):
            # print(monkey)
            monkey['activity'] += len(monkey['items'])
            for item in monkey['items']:
                op_level = monkey['operation'](item)
                new_level = op_level % common_divisor
                # print(f'op_level: {op_level}, new: {new_level}')
                if test(new_level, monkey['test_div']):
                    monkeys[monkey['test_res_true']]['items'].append(new_level)
                else:
                    # print(f'monkey {j} throws {new_level}')
                    monkeys[monkey['test_res_false']]['items'].append(new_level)
            monkey['items'] = []

    print(sorted([monkey['activity'] for monkey in monkeys]))

if __name__ == "__main__":
    main()
