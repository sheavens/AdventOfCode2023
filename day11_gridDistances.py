# Find the sum of the Manhattan distances between each pair of filled cells in a grid.
# Part 2.  Replace each empty row or column with 1,000,000 (1m) empty rows or columns, and 
# repeat this.

testData = [
'...#......',
'.......#..',
'#.........',
'..........',
'......#...',
'.#........',
'.........#',
'..........',
'.......#..',
'#...#.....',
]

data = [readLine.strip() for readLine in open('day11_input.txt', 'r')]

def manhattan( a, b ):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

isEmpty = lambda row: all([c == '.' for c in row])


def solvItPart1(data=testData) : 

    # add one empty row for each empty row in the grid
    emptyRow = ['.' for c in data[0]]
    gridRows = [[c for c in line] for line in data]
    # copy the rows to work on an unchaging grid
    savedRows = gridRows.copy()
    gridRows = []
    for row in savedRows:
        if isEmpty(row):
            empty = emptyRow.copy()
            gridRows.append(empty)
        gridRows.append(row)

    # extract the columns from the revised rows
    gridCols = [[row[i] for row in gridRows] for i in range(len(gridRows[0]))]
    # add one empty column for each empty column in the grid
    emptyCol = ['.' for c in range(len(gridRows))]
    savedCols = gridCols.copy()
    gridCols = []
    for col in savedCols:
        if isEmpty(col):
            empty = emptyCol.copy()
            gridCols.append(empty)
        gridCols.append(col)

    # reassemble the enlarged grid as rows from the revised columns
    bigGrid = [[col[i] for col in gridCols] for i in range(len(gridCols[0]))]

    # form list of coordinates for eaxh filled cell
    filledCells = [(i,j) for i in range(len(bigGrid)) for j in range(len(bigGrid[0])) if bigGrid[i][j] == '#']

    # find the distance from each filled cell to each other filled cell
    distances = []
    for i, cell in enumerate(filledCells):
        j = i + 1
        while j < len(filledCells):
            distances.append(manhattan(cell, filledCells[j]))
            j = j + 1

    return sum(distances)

print('Part 1 : ',solvItPart1(data)) # 686930


# Part 2
# Replace each empty row or column with 1000000 empty rows or columns
def solvItPart2(data=testData, addRows=100, addCols=100) : 

    # this means every row coordinate will have 1000000 added to the row coordinate for every empty row before it.
    # and every column coordinate will have 1000000 added to the column coordinate for every empty column before it.

    # find the column numbers of the empty columns in the input data
    gridRows = [[c for c in line] for line in data]
    emptyRows = [i for i, row in enumerate(gridRows) if isEmpty(row)]
    gridCols = [[row[i] for row in gridRows] for i in range(len(gridRows[0]))]
    emptyCols = [i for i, col in enumerate(gridCols) if isEmpty(col)]

    # form list of coordinates for each filled cell
    filledCells = [(i,j) for i in range(len(data)) for j in range(len(data[0])) if data[i][j] == '#']

    # adjust the coordinates of filled cells by adding 1000000 times the number of empty rows or columns before it, -1 to account for the empty row or col previously there
    filledCells = [(i + (addRows-1) * len([r for r in range(i) if r in emptyRows]), j + (addCols-1) * len([c for c in range(j) if c in emptyCols])-1) for i, j in filledCells]
    
    # find the Manhattan distance from each filled cell to each other filled cell
    distances = []
    for i, cell in enumerate(filledCells):
        for j in range(i+1, len(filledCells)):
            distances.append(manhattan(cell, filledCells[j]))

    return sum(distances)

print('Part 2 : ',solvItPart2(data, 1000000, 1000000)) # 630728425490