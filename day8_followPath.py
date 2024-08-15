"""Follow a path though a chain of nodes counting the steps to reach the end node.
Part 2 required the number of steps for a list of paths to all reach their end nodes at the same time."""

import re
import math
import numpy as np


testMoves = ['LLR']
testPaths = [
'AAA = (BBB, BBB)',
'BBB = (AAA, ZZZ)',
'ZZZ = (ZZZ, ZZZ)'
]

regex = re.compile(r'(\w+) = \((\w+), (\w+)\)')

def paths_to_dict(paths):
    path_dict = {}
    for path in paths:
        fr, toLeft, toRight = regex.findall(path)[0]
        path_dict[fr] = (toLeft, toRight)

        """       path = path.split(' = ')
        left, right = path[1].split(', ')
        d[path[0]] = (left, right) """

    return path_dict

# print(paths_to_dict(testPaths))

def solvitPart1(moves, paths):
    next = 'AAA'
    index = 0
    count = 0
    while next != 'ZZZ':
        count += 1
        m = moves[index]
        if m == 'L':
            next = paths[next][0]
        elif m == 'R':
            next = paths[next][1]
        else:
            print('error')
        index += 1
        if index == len(moves):
            index = 0
    return count

readLines = lambda filename : [line.rstrip('\n') for line in open(filename, 'r')]
lines = readLines('day8_input.txt')

moves = [*lines[0]]
pathDict = paths_to_dict(lines[2:])

# test lines
# moves = [*testMoves[0]]
# pathDict = paths_to_dict(testPaths)

print('Part 1 : ',solvitPart1(moves, pathDict))

# Part 2

testPart2Moves = ['LR']
testPart2Paths = [
'11A = (11B, XXX)',
'11B = (XXX, 11Z)',
'11Z = (11B, XXX)',
'22A = (22B, XXX)',
'22B = (22C, 22C)',
'22C = (22Z, 22Z)',
'22Z = (22B, 22B)',
'XXX = (XXX, XXX)',
]
# to use test lines :
# moves = [*testPart2Moves[0]]
# pathDict = paths_to_dict(testPart2Paths)
       

# calculating all paths to Z in parallel took too long to solve.

# tried using generators, but no obvious improvement (actually not really expected).
    # generator to test for all paths ending in Z
    # def allZ(paths):
    #     nexts = (k for k in paths.keys() if k.endswith('A'))

# try using numpy arrays - no obvious improvement in speed! (unexpected)
    # Ztest = np.vectorize(Ztest)  # Vectorize the Ztest function
    # while not np.all(Ztest''(nexts)): 
    # np.array([paths[next][0] for next in nexts])  # go left

# Instead calculated cycles of intervals for each path reaching '..Z' , which were constant for each. 
# Calculated lowest common multiple - the first time all with have reached '..Z' at the same time.
def solvitPart2(moves, paths):
    allNexts = [k for k in paths.keys() if k.endswith('A')] # [0] FOR TEST JUST TAKE ONE !!!
    index = 0
    Ztest = lambda x : x.endswith('Z')
   
    goRight = lambda next : paths[next][1] 
    goLeft = lambda next : paths[next][0] 

    # test =   # Apply Ztest to all values of nexts
    lastCount = 0
    
    for nexts in allNexts: # take one at a time and record repeat cycle size, because take too long to calculate all step-wize
        print('!!!!!!!!!! ', nexts)
        count = 0
        while (count < 100000): # run a few times to show cycle interval constant
            if np.all(Ztest(nexts)): 
                lastInterval = count - lastCount
                print('end in  Zs', lastInterval) #11567, 19637, 15871, 21251, 12643, 19099
                lastCount = count
            count += 1
            if (count % 1000000) == 0: print('count : ', count)
            m = moves[index]
            if m == 'L':
                nexts = goLeft(nexts)   
            elif m == 'R':
                nexts = goRight(nexts) 
            else:
                print('error')
            index += 1
            if index == len(moves):
                index = 0
    return count


# from the results of the above, the cycle intervals are :
cycleIntervals = [11567, 19637, 15871, 21251, 12643, 19099]
lcm = math.lcm(11567, 19637, 15871, 21251, 12643, 19099) 

print('Part 2', lcm) # 13133452426987

    