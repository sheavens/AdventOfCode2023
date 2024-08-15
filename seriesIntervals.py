

import re
import math

testHistories = [
'0   3   6   9  12  15',
'1   3   6  10  15  21',
'10  13  16  21  30  45' 
]


readFile = lambda filename : [line.rstrip('\n') for line in open(filename, 'r')]

regex = re.compile(r'(\d+)')

testInput = [[int(num) for num in regex.findall(t)] for t in testHistories]

finalValue = lambda series : series[len(series)-1]

def solvitPart1(history=testInput) :
    intervals = []
    for h in history: 
        allSeries = []
        series = h.copy()
        allSeries.append(series)
        while not sum(series) == 0:
            prevSeries = series.copy()
            series = []
            for i in range(len(prevSeries)-1):
                series.append(prevSeries[i+1] - prevSeries[i])
            allSeries.append(series)
        allSeries[len(allSeries)-1].append(0) # add a zero to the end of the series of zeros
        for j in range(len(allSeries)-2,0,-1):
            print(j)
           
            allSeries[j].append(finalValue(allSeries[j])+finalValue(allSeries[j-1]))



    return allSeries



print('Part 1: ',solvitPart1(testInput))
