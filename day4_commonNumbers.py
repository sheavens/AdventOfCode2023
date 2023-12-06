""" Input is list of cards with wnning numbers and numbers on the cards. 
In Part 1, find the sum of the the scores from winning number on each card.
Part 2 each win wins copies of the following 'number of wins cards'. calculate the total number
of cards by the end"""

testInput = [
'Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53',
'Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19',
'Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1',
'Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83',
'Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36',
'Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11',
]

def read_input(filename):
    open_file = open(filename, 'r')
    input = open_file.readlines()
    open_file.close()
    return input

def getScore(num_winners):
    score = 0
    if (num_winners == 0 or num_winners == 1): 
        return num_winners
    else :
        score = 1    
    for num in range(num_winners-1):
        score *= 2
    return score

def solveItPart1(input=testInput):
    total = 0
    for line in input:
        winners = [int(w.strip()) for w in line.split(':')[1].split('|')[0].split()]
        myCards = [int(w.strip()) for w in line.split(':')[1].split('|')[1].split()]
        num_winners = len(set(winners).intersection(set(myCards)))
        score = getScore(int(num_winners))
        total += score
    return total

#print("Part 1 test ", solveItPart1())
print("Part 1 ", solveItPart1(read_input('day4_input.txt')))

def cleanInput(line):
    print(line.split(':')[1].split('|')[0].split())
    winners = [int(w.strip()) for w in line.split(':')[1].split('|')[0].split()]
    myCards = [int(w.strip()) for w in line.split(':')[1].split('|')[1].split()]
    return (winners, myCards)

def getcopies(win_arr):
    copies = [int(1) for w in win_arr] # start with 1 copy of each card
    for i in range(len(win_arr)):
        for j in range(int(win_arr[i])):
            copies[i+1+j] += copies[i] # add 1 to the number of copies of the next 'number of winners' cards
    return copies

def get_num_winners(input=testInput):
    win_arr = []
    for line in input:
        winners, myCards = cleanInput(line)
        win_arr.append(len(set(winners).intersection(set(myCards))))
    return win_arr
   
def solveItPart2(input=testInput):
    win_arr = get_num_winners(input)
    copies_arr = getcopies(win_arr)
    return sum(copies_arr)

#print("Part 2 test ", solveItPart2())
print("Part 2 ", solveItPart2(read_input('day4_input.txt')))