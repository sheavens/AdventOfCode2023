""" Place the code into the strips, and count the ways of doing it. 
Code 1,1,3 indicates a pattern of 1,1 and 3 filled cells must be placed in the strip,
separated by at least one space.  The strip already contains filled cells and spaces
(# and '.', which must remain so in the final strip).  '?' in the strip can become
either a filled cell or a space.  
Part 2 is the same, but the strip is repeated 5 times, with a '?' between each strip.
abd the code is repeated 5 times."""

testData = [
'???.### 1,1,3',
'.??..??...?##. 1,1,3',
'?#?#?#?#?#?#?#? 1,3,1,6',
'????.#...#... 4,1,1',
'????.######..#####. 1,6,5',
'?###???????? 3,2,1',
]

def prepareData(data) :
    lines = []
    codes = []
    for line in data:
        strip, code = line.split(' ')
        lines.append(list(strip))
        code = [int(c) for c in code.split(',')]
        codes.append(code)
    return lines, codes

    
def filledCount(strip) :
    return sum(x == '#' for x in strip)
   
def noHashes(line, i):
    previousHashes = [line[j] for j in range(i) if line[j] == '#'] 
    if len(previousHashes) == 0 : 
        return True
    return False


def placeStrip(line, code, end=True, memo = {}):
# recursive function counting ways of placing code characters into a strip
# if the code is to be continued, end parameter will be false)
    if (tuple(line), tuple(code)) in memo:
        return memo[(tuple(line), tuple(code))]

    # if no value in code, return 
    if code == []:
        # success case if there are no more hashes in the line
        if line == [] or noHashes(line, len(line)):
            return 1
        return 0
    # if there is a code value but no line left to place the strip(s), return 0
    if line == []:
        return 0

    count = 0
    stripLen = code[0]
    i = 0

    # find next possible place to put filled strip of length code[0]
    # there are no more places if there are hashes before the strip
    while i + stripLen <= len(line) and noHashes(line, i): 
        if line[i] in ['#', '?']:
            valid = True
            for j in range(i + 1, i + stripLen):
                if line[j] not in ['#', '?']:
                    valid = False
                    break
            if valid:
                if i + stripLen == len(line) : 
                    if end :
                        count += placeStrip([], code[1:], end, memo)
                elif line[i + stripLen] in ['.', '?']:
                    # recurse to place the next strip after the space
                    count += placeStrip(line[i+stripLen+1:], code[1:], end, memo) # !!! will fail if the line is only 1 longer
        i += 1
    
        memo[(tuple(line), tuple(code))] = count
    return count
    
def solvItPart1(data):
    lines, codes = prepareData(data)
    # lines, codes = prepareData(testData)

    counts = []
    for line, code in zip(lines, codes):
        counts.append(placeStrip(line, code))
    return sum(counts)

print('Part 1: ', solvItPart1(open('day12_input.txt', 'r').readlines())) # 7090


data = open('day12_input.txt', 'r').readlines()
# data = testData


def extendCode(data):
    lines, codes = prepareData(data)
    count = 0
    totalCount = 0
    for line, code in zip(lines, codes) :
        longLine = (line + ['?'])*4+line
        longcode = code *5
        count = placeStrip(longLine, longcode)
        totalCount = totalCount + count
    return totalCount
 

def solvItPart2(data):
    # now strip is repeated 5 times, joined by 1 '?' and code is repeated 5 times
    # same code sufficed with memo added to placestrip function to avoid repeat calculations.
    return extendCode(data)

print('Part 2: ', solvItPart2(data)) # 6792010726878





                  

    






