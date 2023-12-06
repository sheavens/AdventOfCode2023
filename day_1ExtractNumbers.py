""" Combine the first and last digit of each line in the input file and return the sum of all the numbers. 
Part 2 includes numbers one to nine written in words."""

import re

""" Part 2 included numbers with overlapping spelling such as oneight which should be extracted as ['one' 'eight']
text = 'oneight'
matches = re.findall(r'(?=(one|eight))', text)  # (?=...) is a lookahead assertion, means it will pick up overlapping matches
print('test matches',text, matches) """

def extract_numbers(lines):

    combined_numbers = []
    for line in lines:
        digits = re.findall(r'\d', line)
        combined_number = int(digits[0] + digits[-1])
        combined_numbers.append(combined_number)

    total_numbers = sum(combined_numbers)

    return total_numbers

def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        return lines

testLinesPart2 = [
'two1nine',
'eightwothree',
'abcone2threexyz',
'xtwone3four',
'4nineeightseven2',
'zoneight234',
'7pqrstsixteeni',
]

test = ['foursixtwoninevtzzgntnlg6oneightbxp']

def convert_spellings_to_digits(word):
    spellings_to_digits = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    return spellings_to_digits.get(word, word)

def extract_numbers_with_spellings(lines):
    combined_numbers = []

    for line in lines:
        digits = re.findall(r'(?=(\d|one|two|three|four|five|six|seven|eight|nine))', line) # (?=...) means it will pick up overlapping matching words
        digits = [convert_spellings_to_digits(digit) for digit in digits]
        combined_number = int(digits[0] + digits[-1])
        combined_numbers.append(combined_number)

    total_numbers = sum(combined_numbers)

    return total_numbers

input_file_path = "day1_input.txt"
lines = read_input_file(input_file_path)

# Part1
print('Part1 : ', extract_numbers(lines)) # 54644

#Part2
print('Part2 : ', extract_numbers_with_spellings(lines)) # 53348
# print('Part2 test : ', extract_numbers_with_spellings(testLinesPart2)) 
# print('Part2 test overlapping: ', extract_numbers_with_spellings(['oneight']))











