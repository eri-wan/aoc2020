import numpy as np
import re

inputfile = "input"

alphabet = "abcdefghijklmnopqrstuvwxyz"

neighbouring_coordinates = [np.array((1, 1, 1, 1), dtype=int) - (i % 3, (i // 3) % 3, (i // 9) % 3, i // 27) for i in
                            range(3 * 3 * 3 * 3) if i != (27 * 3) // 2]


def append_if_exists(dictionary: dict, key, val):
    if key not in dictionary.keys():
        dictionary[key] = []

    dictionary[key].append(val)



def main():
    # lines = []
    # with open(inputfile) as infile:
    #     while True:
    #         line = infile.readline()
    #         if not line:
    #             break
    #         lines.append(line.strip())
    #
    # print(f"Read {len(lines)} lines")

    # starting_order = "389125467"
    starting_order = "398254716"

    numbers = [int(char) for char in starting_order]  # + list(np.arange(len(starting_order) + 1, 1000001))

    number_indices = np.zeros_like(numbers)
    index_numbers = {}
    for index, number in enumerate(numbers):
        number_indices[number] = index
        index_numbers[index] = number

    print(f"first 20 numbers: {numbers[:20]}")

    iterations = 10
    total_num_items = len(numbers)

    select = 0

    for count in range(iterations):

        choose = numbers[select]
        # print(choose)

        pickup = numbers[select + 1: select + 4]
        if select + 4 > total_num_items:
            num_beginning = select + 4 - total_num_items
            pickup = pickup + numbers[:num_beginning]
            del numbers[:num_beginning]
            select -= num_beginning

        del numbers[select + 1: select + 4]

        # print(numbers)
        # print(pickup)

        destination = (choose - 2) % total_num_items + 1
        # print(destination)
        while destination in pickup:
            destination = (destination - 2) % total_num_items + 1
            # print(destination)
        where = numbers.index(destination)

        numbers[where+1:where+1] = pickup
        if select < where:
            select = (select + 1) % len(numbers)
        else:
            select = (select + 4) % len(numbers)


    final_place_of_choose = iterations % len(numbers)
    numbers = numbers[-final_place_of_choose:] + numbers[:-final_place_of_choose]

    print(numbers)

    # numbers = [int(char) for char in starting_order]  # + list(np.arange(len(starting_order) + 1, 1000001))
    # number_indices = np.zeros_like(numbers)
    # index_numbers = {}
    # for index, number in enumerate(numbers):
    #     number_indices[number - 1] = index
    #     index_numbers[index] = number
    #
    # print(f"first 20 numbers: {numbers[:20]}")
    #
    # iterations = 10
    # total_num_items = len(numbers)
    #
    # select = 0
    #
    # for count in range(iterations):
    #     current_index = count % total_num_items
    #     choose = number_indices.where(number_indices == current_index)
    #     # print(choose)
    #
    #     pickup = [number_indices.where(number_indices == current_index + 1),
    #               number_indices.where(number_indices == current_index + 2),
    #               number_indices.where(number_indices == current_index + 3)]
    #
    #     # print(numbers)
    #     # print(pickup)
    #
    #     destination = (choose - 1) % total_num_items
    #     while destination in pickup:
    #         destination = (destination - 1) % total_num_items
    #         # print(destination)
    #     where = number_indices[destination]
    #
    #     if current_index < where:
    #         between = number_indices > current_index & number_indices < where
    #         number_indices[between] -= 3
    #     else:
    #         select = (select + 4) % len(numbers)
    #     # print(numbers)
    #
    #
    #
    # index_of_one = numbers.index(1)
    #
    # print(f"index of one: {numbers[index_of_one-2:index_of_one+3]}")


if __name__ == "__main__":
    main()
