""" Input is a grid of numbers and symbols. 
Part 1, find the sum of numbers which are touching a symbol.
Part 2, find the sum of products of any two numbers which are touching a star."""


grid = [
    "467..114..",
    "...*......",
    "..35..633.",
    "......#...",
    "617*......",
    ".....+.58.",
    "..592.....",
    "......755.",
    "...$.*....",
    ".664.598.."
]

def get_neighbours(grid, x, y):
    return get_values(grid, get_neighbour_coordinates(grid, x, y))

def get_neighbour_coordinates(grid, x, y): # neat form which filters out the off-grid points at the end..
    neighbours = [
        (x - 1, y),
        (x + 1, y),
        (x, y + 1),
        (x, y - 1),
        (x - 1, y + 1),
        (x - 1, y - 1),
        (x + 1, y + 1),
        (x + 1, y - 1)
    ]
    neighbours = [neighbour for neighbour in neighbours if neighbour[0] >= 0 and neighbour[0] < len(grid) and neighbour[1] >= 0 and neighbour[1] < len(grid[0])]
    return neighbours

def get_values(grid, coordinates):
    return [grid[coordinate[0]][coordinate[1]] for coordinate in coordinates]

def find_valid_numbers(grid):
    valid_numbers = []
    for i in range(len(grid)):
        line = grid[i]
        neighbours = []
        num = ''
        for j in range(len(line)):
            if line[j].isdigit():
                neighbours = neighbours + get_neighbours(grid, i, j)
                num = num + line[j]
            else: 
                symbols = [n for n in neighbours if (n != '.' and n.isdigit() == False)]
                if len(symbols) > 0: # There must be a symbol touching the number somewhere, to be valid
                    valid_numbers.append(int(num))
                neighbours = []
                num = ''
        # the last number in the line
        symbols = [n for n in neighbours if (n != '.' and n.isdigit() == False)]
        if len(symbols) > 0: # There must be a symbol touching the number somewhere, to be valid
            valid_numbers.append(int(num))
        neighbours = []
        num = ''   
    return valid_numbers

#print(sum(find_valid_numbers(grid)))

#open a file and read it into a list by line
def read_grid(filename):
    grid = []
    with open(filename, "r") as f:
        for line in f:
            grid.append(line.strip())
    return grid

#Part 1
print('Part 1 : ', sum(find_valid_numbers(grid=read_grid("day3_input.txt"))))

# Part 2
def find_star_coordinates(grid):
    star_coordinates = []
    for i in range(len(grid)):
        line = grid[i]
        for j in range(len(line)):
            if line[j] == '*':
                star_coordinates.append((i, j))
    return star_coordinates

star_coordinates = find_star_coordinates(grid)
#print(star_coordinates)

def find_star_neighbours(grid):
    star_coordinates = find_star_coordinates(grid)
    star_dict = {} # a dictionary of star coordinates as keys and a list of neighbouring numbers as values
    for i in range(len(grid)):
        line = grid[i]
        neighbours = set()
        num = ''
        for j in range(len(line)):
            if line[j].isdigit():
                neighbours = neighbours.union(set(get_neighbour_coordinates(grid, i, j)))
                num = num + line[j]
            else: 
                # add the coordinates of neibours containing starts as key in a ddiscionary
                # add the num value to a list against that coordinate key. 
                star_neighbours = [n for n in neighbours if n in star_coordinates]
                if len(star_neighbours) > 0:
                    for sn in star_neighbours:
                        if sn in star_dict:
                            star_dict[sn].append(num)
                        else:
                            star_dict[sn] = [num]
                neighbours = set()
                num = ''
        # the last number in the line
        star_neighbours = [n for n in neighbours if n in star_coordinates]
        if len(star_neighbours) > 0:
            for sn in star_neighbours:
                if sn in star_dict:
                    star_dict[sn].append(num)
                else:
                    star_dict[sn] = [num]  
    return star_dict

def get_gear_ratio(star_dict):
    gear_ratio = 0
    sum_gear_ratio = 0
    for key in star_dict:
        if len(star_dict[key]) == 2:
            gear_ratio = int(star_dict[key][0]) * int(star_dict[key][1])
            sum_gear_ratio += gear_ratio
    return sum_gear_ratio

# print(get_gear_ratio(find_star_neighbours(grid)))

#Part 2
print('Part 2 :', get_gear_ratio(find_star_neighbours(grid=read_grid("day3_input.txt")))) # 81997870


