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


def recursive_combat(configurations, player1, player2):
    this_configuration = (tuple(player1), tuple(player2))
    if this_configuration in configurations:
        raise ValueError("PLAYER 1 WINS!!!!")
    else:
        configurations.add(this_configuration)

    if (len(player1) > player1[0]) and (len(player2) > player2[0]):
        player1cop = player1[1:player1[0] + 1].copy()
        player2cop = player2[1:player2[0] + 1].copy()
        new_configuration = set()
        # print(f"Entering sub-game with {player1cop} vs {player2cop}")
        try:
            while len(player1cop) > 0 and len(player2cop) > 0:
                winnername = recursive_combat(new_configuration, player1cop, player2cop)

                p1 = player1cop.pop(0)
                p2 = player2cop.pop(0)
                if winnername != "p2":
                    player1cop += [p1, p2]
                else:
                    player2cop += [p2, p1]
        except ValueError as e:
            pass
        return "p1" if len(player1cop) != 0 else "p2"

    else:
        return "p1" if player1[0] > player2[0] else "p2"



def main():
    lines = []
    with open(inputfile) as infile:
        while True:
            line = infile.readline()
            if not line:
                break
            lines.append(line.strip())

    print(f"Read {len(lines)} lines")

    empty_line = len(lines) // 2
    assert lines[empty_line] == ""
    player1 = []
    for line in lines[1:empty_line]:
        player1.append(int(line))

    player2 = []
    for line in lines[empty_line + 2:]:
        player2.append(int(line))


    player1_next = player1.copy()
    player2_next = player2.copy()
    count = 0
    while len(player1) > 0 and len(player2) > 0:
        count += 1
        p1 = player1.pop(0)
        p2 = player2.pop(0)
        if p1 > p2:
            player1 += [p1, p2]
        else:
            player2 += [p2, p1]

    if len(player1) == 0:
        winner = player2
        winname = "Player 2"
    else:
        assert len(player2) == 0
        winner = player1
        winname = "Player 1"

    score = 0
    for number, entry in enumerate(reversed(winner)):
        score += (number + 1) * entry

    print(f"{winname} won with score {score} after {count} rounds. Deck: {winner}")

    player1 = player1_next
    player2 = player2_next

    configurations = set()
    count = 0
    try:
        while len(player1) > 0 and len(player2) > 0:
            count += 1

            winnername = recursive_combat(configurations, player1, player2)

            p1 = player1.pop(0)
            p2 = player2.pop(0)
            if winnername != "p2":
                player1 += [p1, p2]
            else:
                player2 += [p2, p1]
    except ValueError as e:
        print(e)

    if len(player1) != 0:
        winner = player1
        winname = "Player 1"
    else:
        assert len(player1) == 0
        winner = player2
        winname = "Player 2"

    score = 0
    for number, entry in enumerate(reversed(winner)):
        score += (number + 1) * entry

    print(f"{winname} won with score {score} after {count} rounds. Deck: {winner}")

if __name__ == "__main__":
    main()
