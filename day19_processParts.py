"""Process a list of parts, following rules to reach the end of the chain when teh part is
accepted or rejected, and in Part 1, return the sum of the parts that are accepted.
In Part 2, the number of distinct combinations of part properties that would lead to a part being accepted is returned.
Each part has a properties x, m, a, s, and the rules are a series of instructions in the form: [x|m|a|s] [<|>] [an integer].
If the part properties satify the rule, then the next named rule is processed, otherwise the following instrction is processed."""

import re

testData =[
'px{a<2006:qkq,m>2090:A,rfg}',
'pv{a>1716:R,A}',
'lnx{m>1548:A,A}',
'rfg{s<537:gd,x>2440:R,A}',
'qs{s>3448:A,lnx}',
'qkq{x<1416:A,crn}',
'crn{x>2662:A,R}',
'in{s<1351:px,qqz}',
'qqz{s>2770:qs,m<1801:hdj,R}',
'gd{a>3333:R,R}',
'hdj{m>838:A,pv}',
'',
'{x=787,m=2655,a=1222,s=2876}',
'{x=1679,m=44,a=2067,s=496}',
'{x=2036,m=264,a=79,s=2244}',
'{x=2461,m=1339,a=466,s=291}',
'{x=2127,m=1623,a=2188,s=1013}',
]


with open('day19_input.txt', 'r') as file:
    data = file.read().splitlines()

# data = testData

# Splitting the data into rules and parts
rules = []
parts = []
for line in data:
    if line == '':
        break
    rules.append(line)    
parts = data[len(rules)+1:]

partRegex = re.compile(r'{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}')
ruleKeyRegex = re.compile(r'(\w+){')
lastRuleRegex = re.compile(r'(\w+)}')
ruleRegex = re.compile(r'(\w)([<>=])(\d+):(\w+)')

partDict = []
for part in parts: 
    partDict = partDict + [{'x':int(aa), 'm':int(bb), 'a':int(cc), 's':int(dd)} for aa,bb,cc,dd in partRegex.findall(part)]

ruleDict = {ruleKeyRegex.findall(rule)[0]: ruleRegex.findall(rule) + (lastRuleRegex.findall(rule)) for rule in rules}

def processIt(processCode, part):
    # The processCode is either a string (A or R or key to another process code) or a list of conditions
    if processCode[0] == 'A' or processCode[0] == 'R': # End of processing; part is accepted or rejected
        return processCode[0]
    if isinstance(processCode[0], str): # process code is a string (other than 'A' or 'R'), which is key to another process code
        return processIt(ruleDict[processCode[0]], part)  # lookup and process the next chain of conditions
    else: # process code is a list of conditions
        property, operator, value, nextRule = processCode[0]
        if operator == '<' and part[property] < int(value) \
            or operator == '>' and part[property] > int(value) \
                or operator == '=' and part[property] == int(value) :
            return processIt([nextRule], part)  # condition is met, so process the next rule
        return processIt(processCode[1:], part) # condition is not met, so process the next condition or string


def solveItPart1(parts, ruleDict):
    # start at rule 'in'
    processCode = ruleDict['in']
    rating = 0
    for part in parts :
        if processIt(processCode, part) == 'A':
                rating += part['x'] + part['m'] + part['a'] + part['s']
    return rating

print('Part 1: ',solveItPart1(partDict, ruleDict))

def modRanges(property, range, rangeDict):
    # adjust the rangeDict value for the propery to witin the 'range
    lo, high = rangeDict[property]
    l, h = range
    newDict = rangeDict.copy()
    newDict[property] = [max(lo,l), min(high,h)]
    return newDict

def solutionRanges(rangeDict, rule, ruleDict, solns = []):
    if rule[0] == 'A' :
        print(rangeDict)
        return solns + [rangeDict]
    if rule[0] == 'R':
        return solns
    if isinstance(rule[0], str):
        print('new rule ', rule[0])
        solns = solutionRanges(rangeDict, ruleDict[rule[0]], ruleDict, solns) 
    else: # next step is conditional
        property, operator, value, nextRule = rule[0]
        if operator == '<' :  
            solns = solutionRanges(modRanges(property, [1, int(value)-1], rangeDict), [nextRule], ruleDict, solns) 
            solns = solutionRanges(modRanges(property, [int(value), 4000], rangeDict), rule[1:], ruleDict, solns)
        elif  operator == '>' :
            solns = solutionRanges(modRanges(property, [int(value)+1, 4000], rangeDict), [nextRule], ruleDict, solns)
            solns = solutionRanges(modRanges(property, [1, int(value)], rangeDict), rule[1:], ruleDict, solns)
    return solns


def rangeOverlap(range1, range2):
    start = max(range1[0], range2[0])
    end = min(range1[1], range2[1])
    if start <= end:
        return [start, end]
    else:
        return []

def overlap(rangeDict1, rangeDict2):
    # return the overlap between two rangeDicts
    overlapDict = {}
    for key in rangeDict1.keys():
        overlapDict[key] = rangeOverlap(rangeDict1[key], rangeDict2[key])
    return overlapDict

def countSolutions(rangeDict):
    # return the number of solutions for a rangeDict
    count = 1
    for key in rangeDict.keys():
        if len(rangeDict[key]) == 0:
            return 0
        count = count * (rangeDict[key][1] - rangeDict[key][0] + 1)   
    return count
    
def distinctCombinations(solns):
    # add up all distinct solutions from solution ranges.
    # .. all solutions less duplicate combinations from solns
    count = countSolutions(solns[0])
    for i in range(1, len(solns)):
        for j in range(i):
            overlapDict = overlap(solns[i], solns[j])
            if overlapDict != {}:
                print(' deductions ', countSolutions(overlapDict)) # No overlaps ever counted! and I thought would need to deal with overlaps on overlaps too!
                count -= countSolutions(overlapDict)
        count += countSolutions(solns[i])
    return count

def solveItPart2(ruleDict):
    rangeDict = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}
    #!! distinct ranges; can overlap for different solutions !!
    solns = solutionRanges(rangeDict, ruleDict['in'], ruleDict)
    dc = distinctCombinations(solns)
    return dc

print('Part 2: ',solveItPart2(ruleDict)) #117954800808317
    




