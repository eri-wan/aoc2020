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
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    allergen_candidates = {}
    cannot_be_allergen = {}
    all_ingredients = set()

    for line in lines:
        parts = line.split(" (contains ")
        ingredients = set(parts[0].split(" "))
        allergens = parts[1][:-1].split(", ")
        all_ingredients.update(ingredients)

        for allergen in allergens:
            if allergen not in allergen_candidates.keys():
                allergen_candidates[allergen] = set()
                cannot_be_allergen[allergen] = set()

                allergen_candidates[allergen].update(ingredients)

            cannot_be_allergen[allergen].update(allergen_candidates[allergen].difference(ingredients))
            allergen_candidates[allergen].intersection_update(ingredients)

    not_allergen = all_ingredients.copy()
    for allergen, its_allergen_candidates in allergen_candidates.items():
        not_allergen.difference_update(its_allergen_candidates)

    wrong_approach = set()
    for allergen, not_allergen_candidate in cannot_be_allergen.items():
        print(f"Coan be {allergen}: {allergen_candidates[allergen]}")
        if len(wrong_approach) == 0:
            wrong_approach.update(cannot_be_allergen[allergen])
        else:
            wrong_approach.intersection_update(cannot_be_allergen[allergen])


    count = 0
    for line in lines:
        parts = line.split(" (contains ")
        ingredients = set(parts[0].split(" "))
        for is_not_allergen in not_allergen:
            count += is_not_allergen in ingredients

    print(f"Number of non-allergen items: {len(not_allergen)}, count appear: {count} ({not_allergen})")
    print(f"Other approach: {len(wrong_approach)}: {wrong_approach}")

if __name__ == "__main__":
    main()
