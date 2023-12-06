"""Calculate the number of ways to  beat the course record for a race, by choosing how long to press the charge button for
at the start of the race.  Each nillisecond of charging takes up a ms of race time gives a 1ms/s boost to the speed of the racer for
the rest of the race.
The data dives the duration of races and the record time."""

import math

def count_whole_numbers(a, b, c):

    small_winning_margin = 0.000000002
    c = c+ small_winning_margin
    root = math.sqrt(b**2 - 4*a*c)
    top = (-b + root)/2*a
    bottom = (-b - root)/2*a

    rng = range(math.ceil(bottom),math.floor(top)+1) # +1 to include the last number
    return len(rng)


# Test data
times = [7, 15, 30]
distances = [9, 40, 200]
testRaceData = list(zip(times, distances))

# Part 1 data
times = [54,     70,     82,     75]
distances =  [239,   1142,   1295,   1253]
raceData = list(zip(times, distances))

def solveIt(raceData) :
    # I solved this by finding the roots of the quadratic equation bracketing the race record.
    mult = 1
    for raceDuration, recordDistance in raceData:
        count = count_whole_numbers(1, -1*raceDuration, recordDistance)
        mult *= count
    return mult

print('Part 1 :', solveIt(raceData))

# Part 2 is a single long race, distances and times from concatenating the numbers in the input data.
# Part 2 needed no further coding, as this method already avoids calculating all the winning race times.
def concat(integerList):
    charNumber = ''.join(str(n) for n in integerList)
    return int(charNumber)

raceData2 = (concat(times), concat(distances))

print('Part2: ', solveIt([raceData2]))


