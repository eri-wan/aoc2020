import numpy as np
import re

inputfile = "input15"
example = '''Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3'''

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

def get_interval_at_line(line_y, source, beacon):
    manhattan_distance = np.sum(abs(np.array(source) - beacon))

    dist_y = abs(source[1] - line_y)
    length_at_line = manhattan_distance - dist_y
    if length_at_line < 0:
        return [source[0], source[0]]
    interval_start = source[0] - length_at_line
    interval_end = source[0] + length_at_line + 1
    return [interval_start, interval_end]

def check_first_overlap_in_second(first, second):
    return not(first[0] > second[1] or first[1] < second[0])

def union_overlapping(first, second):
    return [min(first[0], second[0]), max(first[1], second[1])]

def union_all_overlapping_intervals(intervals):
    unionized_intervals = []
    sorted_intervals = sorted(intervals)

    previous_interval = sorted_intervals[0]

    for next_interval in sorted_intervals[1:]:
        if check_first_overlap_in_second(previous_interval, next_interval):
            previous_interval = union_overlapping(previous_interval, next_interval)
        else:
            unionized_intervals.append(previous_interval)
            previous_interval = next_interval
    unionized_intervals.append(previous_interval)

    return unionized_intervals

def remove_beacon(unionized_intervals, beacon_x):
    output_intervals = []
    for interval in unionized_intervals:
        if interval[0] <= beacon_x and beacon_x < interval[1]:
            output_intervals.append((interval[0], beacon_x))
            output_intervals.append((beacon_x + 1, interval[1]))
        else:
            output_intervals.append(interval)
    return output_intervals

def count_sum_interval_length(intervals):
    return sum(interval[1] - interval[0] for interval in intervals)

 
def main():
    import sys
    lines = []
    if len(sys.argv) > 1 and sys.argv[1] == '--example':
        lines = example.splitlines()
        y_line = 10
    else: 
        file_contents = ''
        with open(inputfile) as infile:
            file_contents = infile.read()
        
        lines = file_contents.splitlines() 
        y_line = 2000000

    print(f"Read {len(lines)} lines")

    sources = []
    for line in lines:
        parts = line.split('=')
        sensor_x = int(parts[1].split(',')[0])
        sensor_y = int(parts[2].split(':')[0])
        beacon_x = int(parts[3].split(',')[0])
        beacon_y = int(parts[4])
        sources.append([(sensor_x,sensor_y), (beacon_x, beacon_y)])
    
    intervals = []
    for source, beacon in sources:
        intervals.append(get_interval_at_line(y_line, source, beacon))
    
    unionized_intervals = union_all_overlapping_intervals(intervals)
    print(f'unionized intervals: {unionized_intervals}')
    line_beacons = [beacon[0] for source, beacon in sources if beacon[1] == y_line]
    print(line_beacons)
    for line_beacon in line_beacons:
        unionized_intervals = remove_beacon(unionized_intervals, line_beacon)
    print(f'removed beacons: {unionized_intervals}')

    tot_len = count_sum_interval_length(unionized_intervals)
    print(f'Total length: {tot_len}')

    end_x = 4000000 + 1

    for y_line in range(4000001):
        intervals = []
        ignore_line = False
        for source, beacon in sources:
            interval = get_interval_at_line(y_line, source, beacon)
            intervals.append(interval)
            if interval[0] <= 0 and interval[1] >= end_x:
                ignore_line = True
                break
        if ignore_line:
            continue
        for line_beacon_x in [beacon[0] for source, beacon in sources if beacon[1] == y_line]:
            intervals.append([line_beacon_x, line_beacon_x + 1])
        unionized_intervals = union_all_overlapping_intervals(intervals)

        current_end_interval = end_x
        for interval in unionized_intervals:
            if interval[1] < 0:
                continue
            elif interval[1] < end_x:
                print(f'Found! At ({interval[1]},{y_line})')
                print(f'freq: {interval[1] * 4000000 + y_line}')
            else:
                break
        
        if y_line % 10000 == 0:
            print(f'Processed line {y_line}...')
    

if __name__ == "__main__":
    main()
