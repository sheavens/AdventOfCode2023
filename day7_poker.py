"""A game based on poker hands with a list of hands of cards each with a bid.
Hands are valued in order of poker hands highest to lowest: 
five of a kind, four of a kind, full house, three of a kind, two pair, one pair, high card.
Within each category, hands are valued by the value of first card value, then the second, etc.
Hands are ranked weakest to strongest 1 to n where n is the number of hands. 
Part 1 calculates the sum of the hand rank times the bid for each hand.
Part 2 treats Jacks as wild cards which can be used to promote a hand to a higher ranking category,
but values the jack lower than all other cards in the hand."""


testData = [
'32T3K 765',
'T55J5 684',
'KK677 28',
'KTJJT 220',
'QQQJA 483'
]

import re

readFile = lambda filename : [line.rstrip('\n') for line in open(filename, 'r')]

def get_ranks(cards) :
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
             
def getHand(cards) :
    ranks = get_ranks(cards)
    ranksByCount = [ranks[v] for v in ranks]
    listByCount = sorted(ranksByCount, reverse=True)
    return 'fiveOfAKind' if listByCount[0] == 5 else 'fourOfAKind' if listByCount[0] == 4 else 'fullHouse' if listByCount[0] == 3 and listByCount[1] == 2 else 'threeOfAKind' if listByCount[0] == 3 else 'twoPair' if listByCount[0] == 2 and listByCount[1] == 2 else 'onePair' if listByCount[0] == 2 else 'highCard'

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
    strength = list(range(len(inOrder), 0, -1))
    score = [strength[i] * int(inOrder[i][1]) for i in range(len(inOrder))]
    return(sum(score)) 

#print('Part 1 test ', solvitPart1()) 
print('Part 1: ',solvitPart1(readFile('day7_input.txt'))) # 255048101

def getHandPart2(cards) :
    """Jacks are now wild cards to promote the hand to a higher valued category"""
    ranks = get_ranks(cards)
    JCount = ranks['jacks']
    ranksByCount = [ranks[v] for v in ranks if v != 'jacks']
    listByCount = sorted(ranksByCount, reverse=True)
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
    strength = list(range(len(inOrder), 0, -1))
    score = [strength[i] * int(inOrder[i][1]) for i in range(len(inOrder))]
    return(sum(score)) 

#print('Part 2 test : ', solvitPart2()) 
print('Part 2 : ', solvitPart2(readFile('day7_input.txt'))) 










