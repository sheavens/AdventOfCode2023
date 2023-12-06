""" Maps seed values to locations, through a series of intermediate mappings. 
Part 1 requires findins the lowest location for any seed in the list.
Part 2 the same, but with many more seeds as pairs of seed values are now interpreted as
ranges, not indivdual seeds.  Cannot be calculated directly from all seed values - too slow
Instead, backcalculated ranges of output locations, starting from the lowest, through tha mappngs back to the seeds."""

# test data
"""seeds: 79 14 55 13

# maps are read as destination, source, length of ranges, so '58 98 2' maps 2 
# values 58 to 98, 59 to 99

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

import math
import re

seeds = [79, 14, 55, 13]
seedToSoil = [[50, 98, 2], [52, 50, 48]]
soilToFertilizer = [[0, 15, 37], [37, 52, 2], [39, 0, 15]]
fertilizerToWater = [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]]
waterToLight = [[88, 18, 7], [18, 25, 70]]
lightToTemperature = [[45, 77, 23], [81, 45, 19], [68, 64, 13]]
temperatureToHumidity = [[0, 69, 1], [1, 0, 69]]
humidityToLocation = [[60, 56, 37], [56, 93, 4]]

def load_data_lines(lines) :
    """ Load lines into a list of lists of integers, until a blank line is encountered. """
    data = []
    for line in lines:
        if len(line.split()) > 0:
            data.append([int(number) for number in re.findall(r'\d+', line)])
        else:
            break
    return data

def read_input(filename):
    """Reads the input file and returns a data as lists."""
    seeds, seedToSoil, soilToFertilizer = [], [], []
    fertilizerToWater, waterToLight, lightToTemperature = [], [], []
    temperatureToHumidity, humidityToLocation = [], []
    with open(filename) as file:
        lines = file.readlines()
        for index, line in enumerate(lines):
            if re.search('seeds:', line):
                seeds = load_data_lines(lines[index:])[0]
            elif re.search('seed-to-soil map:', line):
                seedToSoil = load_data_lines(lines[index + 1:])
            elif re.search('soil-to-fertilizer map:', line): 
                soilToFertilizer = load_data_lines(lines[index + 1:])
            elif re.search('fertilizer-to-water map:', line):
                fertilizerToWater = load_data_lines(lines[index + 1:])
            elif re.search('water-to-light map:', line):
                waterToLight = load_data_lines(lines[index + 1:])
            elif re.search('light-to-temperature map:', line):
                lightToTemperature = load_data_lines(lines[index + 1:])
            elif re.search('temperature-to-humidity map:', line):
                temperatureToHumidity = load_data_lines(lines[index + 1:])
            elif re.search('humidity-to-location map:', line):
                humidityToLocation = load_data_lines(lines[index + 1:])

    return seeds, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation

def find_in_range(value, ranges):
    for range in ranges:
        start_output_range, start_input_range, range_length = range
        if value >= start_input_range and value < start_input_range + range_length:
            return start_output_range + value - start_input_range
    return value # if no range found, return the original value

def mappingRanges(seeds, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation):
    """Returns the location of the plant based on the seed number, mapped through ranges."""
    lowest_location = math.inf
    for seed in seeds:
        soil = find_in_range(seed, seedToSoil)
        fertilizer = find_in_range(soil, soilToFertilizer)
        water = find_in_range(fertilizer, fertilizerToWater)
        light = find_in_range(water, waterToLight)
        temperature = find_in_range(light, lightToTemperature)
        humidity = find_in_range(temperature, temperatureToHumidity)
        location = find_in_range(humidity, humidityToLocation)
        if location < lowest_location:
            lowest_location = location
    return lowest_location


seeds, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation = read_input('day5_input.txt')
print('Part 1 : ', mappingRanges(seeds, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation))
# Part 1: 621354867  
# 
   
# Part 2            
# 
def part2(seeds, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation):
    lowest_location = math.inf
    # now seeds represent ranges of values; pairs of values are seed range start and length
    seedPairs = [(seeds[i], seeds[i+1]) for i in range(0, len(seeds), 2)]
    seedRange = []
    for pair in seedPairs:
        print('pair ',pair)
        rangeStart, rangeLength = pair
        for seed in range(rangeStart, rangeStart + rangeLength - 1):
            seedRange.append(seed)
        lowest = mappingRanges(seedRange, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation)
    if lowest < lowest_location:
        lowest_location = lowest
        print('new lowest', lowest_location)
    return lowest_location

# print('Part 2 : ', part2(seeds, seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation))                        
# ... too slow.  But only need to calculate the lowest mapped location values.  


def value_in_range(value, range):
    """Returns True if the value is in the range, False otherwise."""
    start, end = range
    return value >= start and value <= end

def find_input_value(value, ranges):
    for range in ranges:
        start_input_range, start_output_range, range_length = range # range data reversed to produce input from output
        if value >= start_input_range and value < start_input_range + range_length:
            return start_output_range + value - start_input_range
    return value # if no range found, return the original value

def fill(ranges):
    """Returns a list with ranges that fill in the gaps between the ranges in the input list."""
    filledIn = []
    ranges.sort(key=lambda x: x[0])
    for index, range in enumerate(ranges):
        if index == 0:
            if range[0] > 0 : 
                filledIn.append([0, range[0] - 1])
                filledIn.append(range)
            else : 
                filledIn.append(range)
        else:
            previousRange = ranges[index - 1]
            if range[0] > previousRange[1] + 1:
                filledIn.append([previousRange[1] + 1, range[0] - 1])
                filledIn.append(range)
            else:
                filledIn.append(range)
    filledIn.append([range[1] + 1, math.inf])
    return filledIn

testRangeData = [[60, 56, 37], [56, 93, 4]]

def get_input_ranges(outRange=[57,92], rangeData=testRangeData):
    """Returns the input ranges that produce the given output range, based on the range data."""
    inpRanges = []
    lowestBoundary, highestBoundary = outRange
    lowBoundary = lowestBoundary
    outputRanges = [[outLo, outLo+length-1] for (outLo, inpLo, length) in rangeData]
    # insert additional output ranges if [0 - INF] not contiguously covered
    outputRanges = fill(outputRanges)

    while (lowBoundary <= highestBoundary):
        rangeLo, rangeHi = [outRng for outRng in outputRanges if value_in_range(lowBoundary, outRng)][0]
        highBoundary = min(rangeHi, highestBoundary)
        # note that find-input-value will fill in ranges that are not covered by the input range data
        inpRanges.append([find_input_value(lowBoundary, rangeData), find_input_value(highBoundary, rangeData)])
        lowBoundary = highBoundary + 1
    return inpRanges

def get_output_ranges(rangeData=testRangeData):
    """Returns the output ranges in the range data."""
    return [[outLo, outLo+length-1] for (outLo, inpLo, length) in rangeData]


""" seedPairs = [79, 14, 55, 13]
seedToSoil = [[50, 98, 2], [52, 50, 48]]
soilToFertilizer = [[0, 15, 37], [37, 52, 2], [39, 0, 15]]
fertilizerToWater = [[49, 53, 8], [0, 11, 42], [42, 0, 7], [57, 7, 4]]
waterToLight = [[88, 18, 7], [18, 25, 70]]
lightToTemperature = [[45, 77, 23], [81, 45, 19], [68, 64, 13]]
temperatureToHumidity = [[0, 69, 1], [1, 0, 69]]
humidityToLocation = [[60, 56, 37], [56, 93, 4]]  """

seedPairs = seeds
def get_lowest_seed_in_range(seedPairs, outputRange):
    # in part 2 the seeds are ranges of seed values, each successive pair of values is a range start and length
    seedPairs = [(seedPairs[i], seedPairs[i+1]) for i in range(0, len(seedPairs), 2)]
    for pair in seedPairs:
        rangeStart, rangeLength = pair
        lo, hi = outputRange
        if lo >= rangeStart and lo < rangeStart + rangeLength - 1 :
            return lo
        if hi >= rangeStart and hi < rangeStart + rangeLength - 1:
            return rangeStart 
        if lo < rangeStart and hi > rangeStart + rangeLength - 1:
            return rangeStart           
    return None

# rangeOrder gives the mapping ranges in backward order from location to seed
rangeOrder = [humidityToLocation, temperatureToHumidity, lightToTemperature, waterToLight, fertilizerToWater, soilToFertilizer, seedToSoil]

def find_lowest_location(outputRange, seedPairs, rangeOrder, index):
    """Returns the lowest location, mapping location ranges back to seeds recursively"""
    lowest = math.inf
     # Base case: no more mapping ranges to process. The suplied range is the range of seed values
    if index == len(rangeOrder):
        
        lowest_seed = get_lowest_seed_in_range(seedPairs, outputRange) # returns lowest seed in range or None if no seed in range
        if lowest_seed:
            return mappingRanges([lowest_seed], seedToSoil, soilToFertilizer, fertilizerToWater, waterToLight, lightToTemperature, temperatureToHumidity, humidityToLocation)
        return None


    inputRanges = get_input_ranges(outputRange, rangeOrder[index])
    print('inputRanges ', inputRanges)
    for inputRange in get_input_ranges(outputRange, rangeOrder[index]) :
        print('inputRange ', inputRange )
        result =  find_lowest_location(inputRange, seedPairs, rangeOrder, index + 1)
        if (result and result < lowest):  # will have to try all the mapped routes to find the best (lowest) seed value
            lowest = result

    return lowest # if no seed found, return false


# Startiing with the 'tolocation map', sort ranges by location value.
# Take the lowest range and find the range values in the previous map that map to it.  These
# may come from different parts of the ranges - so a list of ranges may be returned. 
# Take each of these in turn and repeat (recursively) , going back through the previous ranges until the seeds ranges are is reached.  
# check whether there are seeds in the seed ranges here.  Find the lowest in the range and map it
# back to the location for the seed. Stop.

def solvit() :
    
    humidityToLocation.sort(key=lambda x: x[0])
    for outputRange in fill(get_output_ranges(humidityToLocation)):
        # find the lowest location that maps back to a seed value
        lowest_location = find_lowest_location(outputRange, seedPairs, rangeOrder, 0)
        if lowest_location:
            return lowest_location
    return None

print(solvit()) # 15880236

