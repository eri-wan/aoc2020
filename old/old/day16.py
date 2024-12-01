import numpy as np
import functools

inputfile = "input16"
example = '''Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II'''

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

def calc_distances_from(name: str, valves: dict):
    distances = {}
    visited = set([name])
    search_next = [name]
    distance = 0
    distances[name] = 0
    while len(visited) != len(valves.keys()):
        distance += 1
        search_next_round = []
        for valve in search_next:
            for neighbour in valves[valve]['connections']:
                if neighbour not in visited:
                    visited.add(neighbour)
                    distances[neighbour] = distance
                    search_next_round.append(neighbour)
        search_next = search_next_round
    
    return distances

counter = 0
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

    valves = {}
    for line in lines:
        parts = line.split(' ')
        valve_name = parts[1]
        rate = int(parts[4].split('=')[1][:-1])
        connections = []
        for conn in parts[9:]:
            connections.append(conn.rstrip(','))
        
        valves[valve_name] = {'rate': rate, 'connections': connections}
    
    distances = {}
    for name in valves.keys():
        distances[name] = calc_distances_from(name, valves)
        valves[name]['distances'] = distances[name]
    
    not_visited_strip_zero = frozenset(valve_name for valve_name in valves.keys() if valves[valve_name]['rate'] > 0)
    # not_visited_ones = frozenset(valve_name for valve_name in valves.keys())
    @functools.cache
    def strip_not_reachable(at_valve, minutes_left, not_visited):
        return frozenset(valve_name for valve_name in not_visited if distances[at_valve][valve_name] + 1 <= minutes_left)

    def calc_score_at(at_valve, minutes):
        return valves[at_valve]['rate'] * minutes

    @functools.cache
    def best_score_from_here(at_valve, minutes_left, not_visited):
        global counter
        counter += 1
        if counter % 10000 == 0:
            print(f'done {counter} counts')
        best_score = 0

        for other_valve in not_visited:
            cost = distances[at_valve][other_valve] + 1
            minutes_left_after = minutes_left - cost
            not_visited_and_reachable = strip_not_reachable(other_valve, minutes_left_after, not_visited - frozenset([other_valve]))
            score_from_valve = calc_score_at(other_valve, minutes_left_after)
            # print(f'at: {at_valve}, fo: {other_valve}, mins left: {minutes_left_after}, not_visited_and_reachable: {not_visited_and_reachable}')
            # print(f'get {score_from_valve} from valve')
            score_after_valve = best_score_from_here(other_valve, minutes_left_after, not_visited_and_reachable)
            tot_score = score_from_valve + score_after_valve
            
            best_score = max(tot_score, best_score)
        return best_score

    def sort_inputs(minutes_pair, places_pair):
        if (minutes_pair[0] < minutes_pair[1] or
            (minutes_pair[0] == minutes_pair[1] and places_pair[0] < places_pair[1])):
            return tuple(reversed(minutes_pair)), tuple(reversed(places_pair))
        return minutes_pair, places_pair

    @functools.cache
    def best_pair_score_from_here(minutes_pair, places_pair, not_visited):
        global counter
        counter += 1
        if counter % 10000 == 0:
            print(f'done {counter} counts')
        best_score = max(best_score_from_here(places_pair[0], minutes_pair[0], not_visited), 
                         best_score_from_here(places_pair[1], minutes_pair[1], not_visited))

        for other_valve in not_visited:
            cost = distances[places_pair[0]][other_valve] + 1
            minutes_left_after = minutes_pair[0] - cost
            not_visited_and_reachable_first = strip_not_reachable(other_valve, minutes_left_after, not_visited - frozenset([other_valve]))
            not_visited_and_reachable_second = strip_not_reachable(places_pair[1], minutes_pair[1], not_visited - frozenset([other_valve]))
            score_from_valve = calc_score_at(other_valve, minutes_left_after)
            # print(f'at: {at_valve}, fo: {other_valve}, mins left: {minutes_left_after}, not_visited_and_reachable: {not_visited_and_reachable}')
            # print(f'get {score_from_valve} from valve')
            new_minutes_pair, new_places_pair = sort_inputs((minutes_left_after, minutes_pair[1]), (other_valve, places_pair[1]))
            
            score_after_valve = best_pair_score_from_here(new_minutes_pair, new_places_pair, not_visited_and_reachable_first | not_visited_and_reachable_second)
            tot_score = score_from_valve + score_after_valve
            
            best_score = max(tot_score, best_score)
        return best_score


    best_score = best_score_from_here('AA', 30, not_visited_strip_zero)
    best_score = best_pair_score_from_here((26, 26), ('AA', 'AA'), not_visited_strip_zero)
    print(f'best score: {best_score}')
            




if __name__ == "__main__":
    main()
