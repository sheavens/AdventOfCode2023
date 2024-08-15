"""Find line of reflection within each grid, which may be a vertical or horizontal line between columns or rows.
Score the line of reflection as the sum of the column number of the line of reflection, with the row number multiplied by 100.
Return the sum of the scores for all grids in the input data.
Part 2 requires finding a new line of reflection within each grid by changing one, and only one, point 
from filled to unfiled, or vice-versa"""

import re

testData1 = [
'#.##..##.',
'..#.##.#.',
'##......#',
'##......#',
'..#.##.#.',
'..##..##.',
'#.#.##.#.',
]

testData2 = [
'#...##..#',
'#....#..#',
'..##..###',
'#####.##.',
'#####.##.',
'..##..###',
'#....#..#',
]

data = [[c for c in line] for line in testData2] 

def checkReflect(high, low):
    # returns true if the high and low lists are reflections of each other (excluding outer line if no equivalent line)
    if len(high) == 0 and len(low) == 0:
        return True
    """if len(high) == 0 or len(low) == 0:
        return False"""

    if len(high) > len(low):
        high = high[:len(low)]

    low = low[:-len(high)-1:-1] # reverse the list and take the first len(high) elements

    i = 0
    for l in low:
        if high[i] != l:
            return False 
        i = i + 1
    return True

def aboveCol(col, row):
    # returns true if the point is above the column line
    return lambda i, j: j > col and i == row

def reflectVertical(col, data, numRows):
    # all rows must reflect about this column line to return true
    for row in range(numRows) :  
        rowData = data[row]
        values_above_col = [rowData[j] for j in range(len(rowData)) if j > col]
        values_below_col = [rowData[j] for j in range(len(rowData)) if j < col]
        if not checkReflect(values_above_col, values_below_col):
            return False
    return True


def reflectHorizontal(row, data, numCols):
    # all columns must reflect about this row line to return true
    for col in range(numCols) :
        high = [data[i][j] for i in range(len(data)) for j in range(len(data[0])) if j == col and i > row]
        low = [data[i][j] for i in range(len(data)) for j in range(len(data[0])) if j == col and i < row]
        if not checkReflect(high, low):
            return False
    return True


def reflect(data):

    # test a line for a reflection
    # make new list of coordinates with the x values reflected about x = len(data[0]) // 2
    
    vFlect = 0
    hFlect = 0   
    reflect = False
    for column in range(len(data[0])-1):
        if reflectVertical(column+0.5, data, len(data)):
            # print('column + 1', column + 1)
            vFlect += column + 1
            reflect = True
            break

    if reflect == False:
        for row in range(len(data)-1):
            if reflectHorizontal(row+0.5, data, len(data[0])):
                # print('row + 1', row + 1)
                hFlect += row + 1
                reflect = True
                break
    # Return the sum of the column number of the line of reflection, with the row number multiplied by 100.       
    return vFlect + 100 * hFlect

# print(reflect(data))

def checkReflectOneOut(high, low):
    # returns true if the high and low lists are reflections of each other 
    # with one value only changed (excluding outer line if no equivalent line)
    numOut = 0

    if len(high) == 0 and len(low) == 0:
        return True
    """if len(high) == 0 or len(low) == 0:
        return False"""

    if len(high) > len(low):
        high = high[:len(low)]

    low = low[:-len(high)-1:-1] # reverse the list and take the first len(high) elements

    i = 0
    for l in low:
        if high[i] != l:
            numOut += 1
            if numOut > 1 : 
                return numOut  # will return at 2 if more than one value is different
        i = i + 1
    return numOut # will return 0 or 1

def reflectVerticalOneOut(col, data, numRows):
    # all but one rows must reflect about this column line to return true
    # the other one requires only one point to be changed to reflect
    oneOut = 0
    for row in range(numRows) :  
        rowData = data[row]
        values_above_col = [rowData[j] for j in range(len(rowData)) if j > col]
        values_below_col = [rowData[j] for j in range(len(rowData)) if j < col]
        numOut = checkReflectOneOut(values_above_col, values_below_col) # the number of non-matched points
        if numOut > 1:
            return False # no row can have more than one non-matched point
        elif numOut == 1:
            oneOut += 1
            if oneOut > 1:
                return False # no more than one row can have one non-matched point
    if oneOut == 1:
        return True # one row has one non-matched point
    return False


def reflectHorizontalOneOut(row, data, numCols):
    # all but one columns must reflect about this row line to return true
    # the other one requires only one point to be changed to reflect
    oneOut = 0
    for col in range(numCols) :
        high = [data[i][j] for i in range(len(data)) for j in range(len(data[0])) if j == col and i > row]
        low = [data[i][j] for i in range(len(data)) for j in range(len(data[0])) if j == col and i < row]
        numOut = checkReflectOneOut(high, low) # the number of non-matched points
        if numOut > 1:
            return False # no col can have more than one non-matched point
        elif numOut == 1:
            oneOut += 1
            if oneOut > 1:
                return False # no more than one col can have one non-matched point
    if oneOut == 1:
        return True # one col has one non-matched point
    return False

def correctReflect(data):
    # find a line that would be a line of reflection if one, and only one, point were changed
    # return the result for the revised gris, with this point changed

    vFlect = 0
    hFlect = 0
    
    reflect = False
    for column in range(len(data[0])-1):
        if reflectVerticalOneOut(column+0.5, data, len(data)) :
            # print('column + 1', column + 1)
            vFlect += column + 1
            reflect = True
            break

    if reflect == False:
        for row in range(len(data)-1):
            if reflectHorizontalOneOut(row+0.5, data, len(data[0])) :
                # print('row + 1', row + 1)
                hFlect += row + 1
                reflect = True
                break
    # Return the sum of the column number of the line of reflection, with the row number multiplied by 100.       
    return vFlect + 100 * hFlect

# print(correctReflect(data))

def split_on_empty_lines(s):

    # greedily match 2 or more new-lines
    blank_line_regex = r"(?:\r?\n){2,}"

    return re.split(blank_line_regex, s.strip())


def solveItPart1(input):
    grids = split_on_empty_lines(input)

    score = 0
    for grid in grids:
        # print(grid)
        data = [[c for c in line] for line in grid.split('\n')] 
        s = reflect(data)
        # print(s)
        score += s
    return score

def solveItPart2(input):
    grids = split_on_empty_lines(input)

    score = 0
    for grid in grids:
        # print(grid)
        data = [[c for c in line] for line in grid.split('\n')] 
        s = correctReflect(data)
        # print(s)
        score += s
    return score

print('Part 1: ', solveItPart1(open('day13_input.txt', 'r').read()))  # 27505
print('Part 2: ', solveItPart2(open('day13_input.txt', 'r').read())) # 22906

