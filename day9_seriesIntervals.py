""" calculate the next value in a series by taking the interval 
values of the series, then the intervals of intervals..until intervals are 0, then
working back up to the original series with the next values using the intervals.
Part 2 extrapolates the series backwards """

""" Qute interesting. I think a geometric seties is being reduced to a linear series 
by looking at intervals"""

import re
import math

testHistories = [
'0   3   6   9  12  15',
'1   3   6  10  15  21',
'10  13  16  21  30  45' 
]

testInput = [[int(num) for num in t.split()] for t in testHistories]

""" regex = re.compile(r'(-?\d+)')
test2input = [[int(num) for num in regex.findall(t)] for t in testHistories]
checkSame = [(h, t)  for h,t in zip(testInput,test2input) if h != t] """

finalValue = lambda series : series[len(series)-1]

def solvitPart1(history=testInput) :
    lastValue = 0
    sumLastValue = 0
    cnt = 0
    for h in history: 
        allSeries = []
        series = h.copy()
        allSeries.append(series)
        while not any(series) == 0: # cured bug over sum(series) = 0 if negative numbers included take to 0
            prevSeries = series.copy()
            series = []
            for i in range(len(prevSeries)-1):
                series.append(prevSeries[i+1] - prevSeries[i])
            allSeries = [series.copy()] + allSeries # add to the fromt of allSeries
        allSeries[0].append(0) # add a zero to the end of the series of zeros

        # update the series from the previous series.
        for i in range(1,len(allSeries)) :
            allSeries[i].append(finalValue(allSeries[i])+finalValue(allSeries[i-1]))

        lastValue = finalValue(allSeries[len(allSeries)-1])
        cnt +=1
        sumLastValue = sumLastValue + lastValue
    return sumLastValue




readFile = lambda filename : [line.rstrip('\n') for line in open(filename, 'r')]


testInput = [[int(num) for num in t.split()] for t in testHistories]
history = [[int(num) for num in t.split()] for t in readFile('day9_input.txt')]


print('Part 1: ',solvitPart1(history)) # 1882395907

initialValue = lambda series : series[0]

def solvitPart2(history=testInput) :
    firstValue = 0
    sumFirstValue = 0
    cnt = 0
    for h in history: 
        allSeries = []
        series = h.copy()
        allSeries.append(series)
        while not any(series) == 0: # cured bug over sum(series) = 0 if negative numbers included take to 0
            prevSeries = series.copy()
            series = []
            for i in range(len(prevSeries)-1):
                series.append(prevSeries[i+1] - prevSeries[i])
            allSeries = [series.copy()] + allSeries # add to the fromt of allSeries

        # here on part 2 differs: now calculating the sum of series values extrapolated backwards
        allSeries[0] = [0] + allSeries[0] # add a zero to the front of the series of zeros

        # update the series from the previous series.
        for i in range(1,len(allSeries)) :
            allSeries[i] =  [initialValue(allSeries[i]) - initialValue(allSeries[i-1])] # deducting

        firstValue = initialValue(allSeries[len(allSeries)-1])
        cnt +=1
        sumFirstValue = sumFirstValue + firstValue
    return sumFirstValue

print('Part 2: ',solvitPart2(history)) # 1005
