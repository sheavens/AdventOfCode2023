"""For a game where a bag of cubes containg some number of red, green and blue cubes,
input data gives the number of cubes of each colour pulled out of the bag for
a number of samples (with cubes replaced)
Part 1: Find the games that are possible in the list given the contents of the bag.
Part 2: Find the minimum number of reds, blues and greens that must be present for each game."""

import re

testInput = [
'Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green',
'Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue',
'Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red',
'Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red',
'Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green',
]

gNum = re.compile(r"Game\s+(\d+):")
r = re.compile(r"(\d+)\s+red")
b = re.compile(r"(\d+)\s+blue")
g = re.compile(r"(\d+)\s+green")

def solveItPart1(lines, reds, greens, blues ):
    sumIds = 0
    for line in lines:
        gameNum = gNum.findall(line)
        minReds =  max([int(red) for red in r.findall(line)])
        minBlues = max([int(blue) for blue in b.findall(line)])
        minGreens = max([int(green) for green in g.findall(line)])
        if reds >= minReds and blues >= minBlues and greens >= minGreens :
            sumIds += int(gameNum[0])
    return sumIds   

def solveItPart2(lines, reds, greens, blues ):
    sumPowers = 0
    for line in lines:
        minReds =  max([int(red) for red in r.findall(line)])
        minBlues = max([int(blue) for blue in b.findall(line)])
        minGreens = max([int(green) for green in g.findall(line)])
        power = minReds * minBlues * minGreens
        sumPowers += power
    return sumPowers  

# print(solveItPart1(testInput, 12, 13, 14))
# print(solveItPart2(testInput, 12, 13, 14))

readInput = open("day2_input.txt", "r")
lines = readInput.readlines()

print('Part 1 : ', solveItPart1(lines, 12, 13, 14)) # 2149
print('Part 2 : ', solveItPart2(lines, 12, 13, 14)) # 71274
