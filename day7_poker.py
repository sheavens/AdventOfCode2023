
testData = [
'32T3K 765',
'T55J5 684',
'KK677 28',
'KTJJT 220',
'QQQJA 483',
'99999 1',
'QQQQQ 1',
'12222 1',
'666KQ 1',
'77333 1',
'4563K 1',
'55388 1',
'KKKKK 1',
'AA752 1',
'2AAJA 1'
]

import re

readFile = lambda filename : [line.rstrip('\n') for line in open(filename, 'r')]

def get_suits(cards) :
    aces = re.findall('A', cards)
    kings = re.findall('K', cards)
    queens = re.findall('Q', cards)
    jacks = re.findall('J', cards)
    tens = re.findall('T', cards)
    nines = re.findall('9', cards)
    eghts = re.findall('8', cards)
    sevens = re.findall('7', cards)
    sixes = re.findall('6', cards)
    fives = re.findall('5', cards)
    fours = re.findall('4', cards)
    threes = re.findall('3', cards)
    twos = re.findall('2', cards)
    ones = re.findall('1', cards) 

    return {'aces': len(aces), 'kings' : len(kings), 'queens' : len(queens), 'jacks' : len(jacks), 'tens' : len(tens), \
            'nines' : len(nines), 'eights' : len(eghts), 'sevens' : len(sevens), 'sixes' : len(sixes), \
                'fives' : len(fives), 'fours' : len(fours), 'threes' : len(threes), 'twos' : len(twos), 'ones' : len(ones)}
             

# listByCount = [len(kings), len(queens), len(jacks), len(tens), len(nines), len(eghts), len(sevens), len(sixes), len(fives), len(fours), len(threes), len(twos), len(ones)]

def getHand(cards) :
    suits = get_suits(cards)
    suitsByCount = [suits[v] for v in suits]
    listByCount = sorted(suitsByCount, reverse=True)
    return 'fiveOfAKind' if listByCount[0] == 5 else 'fourOfAKind' if listByCount[0] == 4 else 'fullHouse' if listByCount[0] == 3 and listByCount[1] == 2 else 'threeOfAKind' if listByCount[0] == 3 else 'twoPair' if listByCount[0] == 2 and listByCount[1] == 2 else 'onePair' if listByCount[0] == 2 else 'highCard'

# print('fiveOfAKinds', fiveOfAKinds, 'fourOfAKinds', fourOfAKinds, 'fullHouses', fullHouses, 'threeOfAKinds', threeOfAKinds, 'twoPairs', twoPairs, 'onePairs', onePairs, 'highCards', highCards)


# produce a ket for the sort order of hans of cards
def sortKey(cards) :
    key = ''
    sortSequence = ['A','K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    alphabetOrder = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    sortDict = {sortSequence[i] : alphabetOrder[i] for i in range(len(sortSequence))}
  
    splitCards = list(cards)
    for chr in splitCards:
        keyChar = sortDict.get(chr)
        key += keyChar
    return key


def solvitPart1(input=testData) :
    data = [(cards, bid, getHand(cards)) for cards, bid in [line.split() for line in input]]

    fiveOfAKinds = [(cards, bid, hand) for cards, bid, hand in data if hand == 'fiveOfAKind']
    fourOfAKinds = [(cards, bid, hand) for cards, bid, hand in data if hand == 'fourOfAKind']
    fullHouses = [(cards, bid, hand) for cards, bid, hand in data if hand == 'fullHouse']
    threeOfAKinds = [(cards, bid, hand) for cards, bid, hand in data if hand == 'threeOfAKind']
    twoPairs = [(cards, bid, hand) for cards, bid, hand in data if hand == 'twoPair']
    onePairs = [(cards, bid, hand) for cards, bid, hand in data if hand == 'onePair']
    highCards = [(cards, bid, hand) for cards, bid, hand in data if hand == 'highCard']

    inOrder = []
    inOrder.extend(sorted(fiveOfAKinds, key=lambda x: sortKey(x[0])))
    inOrder.extend(sorted(fourOfAKinds, key=lambda x: sortKey(x[0]))) 
    inOrder.extend(sorted(fullHouses, key=lambda x: sortKey(x[0]))) 
    inOrder.extend(sorted(threeOfAKinds, key=lambda x: sortKey(x[0]))) 
    inOrder.extend(sorted(twoPairs, key=lambda x: sortKey(x[0]))) 
    inOrder.extend(sorted(onePairs, key=lambda x: sortKey(x[0]))) 
    inOrder.extend(sorted(highCards, key=lambda x: sortKey(x[0])))
    
    # Create a list of numbers from the length of inOrder to 1
    rank = list(range(len(inOrder), 0, -1))
    score = [rank[i] * int(inOrder[i][1]) for i in range(len(inOrder))]
    return(sum(score)) 

# print(solvitPart1()) 
print('Part 1: ',solvitPart1(readFile('day7_input.txt'))) # 255048101

def getHandPart2(cards) :
    """Jacks are now wild cards to promote the hand to a higher ranking type"""
    suits = get_suits(cards)
    JCount = suits['jacks']
    suitsByCount = [suits[v] for v in suits if v != 'jacks']
    listByCount = sorted(suitsByCount, reverse=True)
    # add the number of 'J' cards to the highest count
    listByCount[0] += JCount
    return 'fiveOfAKind' if listByCount[0] == 5 else 'fourOfAKind' if listByCount[0] == 4 else 'fullHouse' if listByCount[0] == 3 and listByCount[1] == 2 else 'threeOfAKind' if listByCount[0] == 3 else 'twoPair' if listByCount[0] == 2 and listByCount[1] == 2 else 'onePair' if listByCount[0] == 2 else 'highCard'

def sortKeyPart2(cards) :
    """Jack is now ranked lowest"""
    key = ''
    sortSequence = ['A','K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    alphabetOrder = ['a','b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    sortDict = {sortSequence[i] : alphabetOrder[i] for i in range(len(sortSequence))}

    splitCards = list(cards) 
    for chr in splitCards:
        keyChar = sortDict.get(chr)
        key += keyChar
    return key

def solvitPart2(input=testData) :

    data = [(cards, bid, getHandPart2(cards)) for cards, bid in [line.split() for line in input]]

    fiveOfAKinds = [(cards, bid, hand) for cards, bid, hand in data if hand == 'fiveOfAKind']
    fourOfAKinds = [(cards, bid, hand) for cards, bid, hand in data if hand == 'fourOfAKind']
    fullHouses = [(cards, bid, hand) for cards, bid, hand in data if hand == 'fullHouse']
    threeOfAKinds = [(cards, bid, hand) for cards, bid, hand in data if hand == 'threeOfAKind']
    twoPairs = [(cards, bid, hand) for cards, bid, hand in data if hand == 'twoPair']
    onePairs = [(cards, bid, hand) for cards, bid, hand in data if hand == 'onePair']
    highCards = [(cards, bid, hand) for cards, bid, hand in data if hand == 'highCard']

    inOrder = []
    inOrder.extend(sorted(fiveOfAKinds, key=lambda x: sortKeyPart2(x[0])))
    inOrder.extend(sorted(fourOfAKinds, key=lambda x: sortKeyPart2(x[0]))) 
    inOrder.extend(sorted(fullHouses, key=lambda x: sortKeyPart2(x[0]))) 
    inOrder.extend(sorted(threeOfAKinds, key=lambda x: sortKeyPart2(x[0]))) 
    inOrder.extend(sorted(twoPairs, key=lambda x: sortKeyPart2(x[0]))) 
    inOrder.extend(sorted(onePairs, key=lambda x: sortKeyPart2(x[0]))) 
    inOrder.extend(sorted(highCards, key=lambda x: sortKeyPart2(x[0])))
    
    # Create a list of numbers from the length of inOrder down to 1
    rank = list(range(len(inOrder), 0, -1))
    score = [rank[i] * int(inOrder[i][1]) for i in range(len(inOrder))]
    return(sum(score)) 

#print('Part 2 test : ', solvitPart2()) 
print('Part 2 : ',solvitPart2(readFile('day7_input.txt'))) 










