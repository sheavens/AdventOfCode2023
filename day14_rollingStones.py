"""Tip a tray of stones (marked )) which roll until an edge or barrier(#) is hit.  
Part 1 tilts the tray to the North.
Part 2 tips the tray to the N, W, S and E (one cycle) and requires the position after 1000000000 cycles."""

# Define the map as a list of strings
map_array = [
    "#.#.#",
    "#O..#",
    "##.O#",
    "#...#",
    "#O###"
]

map_array = [
'O....#....',
'O.OO#....#',
'.....##...',
'OO.#O....O',
'.O.....O#.',
'O.#..O.#.#',
'..O..#O..O',
'.......O..',
'#....###..',
'#OO..#....',
]

def printMap(map_array):
    for row in map_array:
        print(row)


def move_stones_north(map_array):
    # Loop over all rows
    for row in range(len(map_array)):
        # Loop over all columns
        for col in range(len(map_array[row])):
            # Check if the current position contains a stone
            if map_array[row][col] == 'O':
                # Move the stone as far North as possible
                r = row
                while r > 0 and (map_array[r-1][col] == '.' ):
                    map_array[r] = map_array[r][:col] + '.' + map_array[r][col+1:]
                    map_array[r-1] = map_array[r-1][:col] + 'O' + map_array[r-1][col+1:]
                    r -= 1
    # Return the map
    return map_array

# printMap(move_stones_north(map_array))

def loadCount(map_array):
    # Return the 'load', being sum of the distances of the stones to the South edge (inc row of stone)
    count = 0
    for row in range(len(map_array)):
        for col in range(len(map_array[row])):
            if map_array[row][col] == 'O':
                count += len(map_array) - row
    return count

# print(' Part 1 test:',loadCount(move_stones_north(map_array)))

def solveItPart1(input) : 
    return loadCount(move_stones_north(input))

print('Part 1: ', solveItPart1(open('day14_input.txt', 'r').readlines())) #  109638

def spinWest90(map_array):
    new_map_array = []
    for col in range(len(map_array[0])):
        new_map_array.append(''.join([map_array[row][col] for row in range(len(map_array))[::-1]]))
    return new_map_array

def find_repeating_pattern(lst):
    patterns = []
    for i in range(1, len(lst)//2 + 1):
        pattern = lst[:i]
        if all(lst[j] == pattern[j % i] for j in range(i, len(lst))):
            patterns.append(pattern)
    return patterns

# print(find_repeating_pattern([1,2,3,1,2,3,1,2,3,1,2,3,1,2,3]))


def solveItPart2(input, cycles = 1000000000) :
    # There are too many cycles to calculate, so we need to find a repeating pattern and use that 
    # to calculate the load at cycle 1000000000
    grid = input
    loadDict = {}
    intervalDict = {}
    for cycle in range(cycles):
        for spins in range(4):
            grid = move_stones_north(grid)
            grid = spinWest90(grid)

        key = str(loadCount(grid))
        # keep a dictionary of the list of cycles at which each load value occurs
        # also keeping a dictionary of the intervals between each load value
        # .. when load values start to repeat, their dictionary entries grow, and may see
        # repeating intervals between load values
        if key not in loadDict:
            loadDict[key] = [cycle+1] 
            intervalDict[key] = []
        else:
            intervalDict[key].append(cycle+1 - loadDict[key][-1])
            loadDict[key].append(cycle+1)

## 102357
        if (cycle + 1) % 100 == 0 : 
            print('cycle+1: ', cycle+1)  
            # toDo: write this to calculate the repeat cycle (21) and the load at 1000000000
            # from the dictionary entries (did this manually) 
            print(1000000000 % 21) # 21 - this was the repeat interval (common to most loads)
            for i in range(121,143) : # these were the start of repeating cycles for different load values
              print(i, i % 21 == 13) # looking for a repeating cycle that will contain 1000000000
              
              # load cycles start to repeat every 21 cycles
              # 1000000000 % 21 is 13
              # repeating cycles in dictionary start at cycles 121-143
              # 139 % 21 is 13 
              # cycle 139 falls into dictionary for load 102356 ..
              # cycle 1000000000 will fall into the same dictionary load 


    print(loadCount(grid))

with open('day14_input.txt', 'r') as file:
    lines = file.read().splitlines()

print('Part 2: ', solveItPart2(lines, 2000)) # got pattern within 2000 cycles
# at 1000000000 cycles load will be 102356
 
