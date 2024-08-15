""" Dig a pit by digging a boundary around a lagoon, then dig out the enclosed cells.
Instructions for digging are given by a series of directions and distances to move.
Part 1: Find the number of cells dug out.
Part 2: As part 1 but now use the Hex colour code given alongside dig instructions,
converted to give new directions and distances to move."""
import math
import queue
from functools import reduce

def flatten(listOfLists):
    return reduce(lambda x,y: x+y, listOfLists)

def neighbours(cell):
    row, col = cell
    return [(row-1, col), (row+1, col), (row, col-1), (row, col+1)]

testData = [
    'R 6 (#70c710)',
    'D 5 (#0dc571)',
    'L 2 (#5713f0)',
    'D 2 (#d2c081)',
    'R 2 (#59c680)',
    'D 2 (#411b91)',
    'L 5 (#8ceee2)',
    'U 2 (#caa173)',
    'L 1 (#1b58a2)',
    'U 2 (#caa171)',
    'R 2 (#7807d2)',
    'U 3 (#a77fa3)',
    'L 2 (#015232)',
    'U 2 (#7a21e3)',
]

testInstructions = [(direction, int(spaces), color) for 
                (direction, spaces, color) in [line.split(' ') for line in testData]]


def sign(value):
    if value > 0:
        return 1
    elif value < 0:
        return -1
    else:
        return 0
 

def joinVertices(list):
    # join the vertices in a list into a continuous boundary
    if list[0] != list[-1]:
        list.append(list[0]) # make it a loop
    fullList = []
    for i in range(len(list)-1) :
        x2, y2 = list[i+1]
        x1, y1 = list[i]
        if x1 == x2 :
            y = y1
            while y != y2 :
                fullList.append((x1, y)) 
                y += sign(y2-y1)
        if y1 == y2 :
            x = x1
            while x != x2 :
                fullList.append((x, y1))
                x += sign(x2-x1)
    return fullList

def printGrid(coordList, vertices = False):
    minRow = min(row for col, row in coordList)
    maxRow = max(row for col, row in coordList)
    minCol = min(col for col, row in coordList)
    maxCol = max(col for col, row in coordList)

    # translate the coordinates to start at 0,0
    coordList = [(col-minCol, row-minRow) for col, row in coordList]
    maxRow = maxRow - minRow
    maxCol = maxCol - minCol
    minRow = 0
    minCol = 0
    # scale down the coordinates to fit on screen 
    coordList = [(int(col/10000), int(row/10000)) for col, row in coordList]
    # coordList = [(int(math.log(col,10)*10), int(math.log(row, 10)*10)) for col, row in coordList if row != 0 and col != 0]
    minRow = min(row for col, row in coordList)
    maxRow = max(row for col, row in coordList)
    minCol = min(col for col, row in coordList)
    maxCol = max(col for col, row in coordList)
    # join the coordinates, if they are vertices, into a continuous of boundary cells
    if vertices:
        coordList = joinVertices(coordList)

    # print the grid
    for row in range(minRow, maxRow+1):
        for col in range(minCol, maxCol+1):
            if (col, row) in coordList:
                print('#', end='')
            else:
                print('.', end='')
        print() # new line at end of row
    print()

def printLogGrid(coordList, vertices = False):
    return [(math.floor(x0/1000), math.floor((x1/1000))) for x0, x1 in coordList]

def floodfill(coordSet, innerCell, boundaryList):
    q = queue.Queue()
    # floodfill empty from this inner cell, with boundary
    if innerCell not in coordSet and innerCell not in boundaryList:  # if this innercell is in the coorset, this inner area has already been filled
        coordSet.add(innerCell)
        q.put(innerCell)
        while not q.empty():
            innerCell = q.get()
            for n in neighbours(innerCell):
                if n not in coordSet and n not in boundaryList:
                    coordSet.add(n)
                    q.put(n)
    # print(len(coordSet))
    return coordSet

def countEnclosedCells(coordSet, boundary):
    # fill in the enclosed cells
    # boundary could be convoluted and a cell could be on both boundaries.
    # 
    # if travelling clockwise around the boundary, inner cells are to the right of the direction of trave.
    # The cell with the leftmost column will be on the leftmost boundary.   Going to the North (or East)
    # will be clockwise.

    # find the leftmost edge on the boundary
    minCol = min(col for row, col in boundary)        
    leftEdge = [(row, col) for row, col in boundary if col == minCol]
    # From an edge cell, go clockwise around the boundary, finding the inner cels along the boundary wall
    startCell = leftEdge[0]
    clockwise = []
    row, col = startCell
    # Clockwise cell is North or East of starting left edge cell
    if (row-1, col) in boundary:
        direction = 'N'
        nextCell = (row-1, col)
    elif (row, col+1) in boundary:
        direction = 'E'
        nextCell = (row, col+1)
    else:
        print('Error: no boundary cell to the North or East of the leftmost edge cell')

    # from a given heading can go to the next boundary cell in these directions (erxcludes reverse direction)  
    fromHereDict = {'N': ['N', 'E', 'W'], 'E' : [ 'E', 'N', 'S'], 
                    'S': ['S', 'E', 'W'], 'W': ['W', 'N', 'S']} 
      
    innerCells = []
    while nextCell != startCell:

        for dir in fromHereDict[direction]: # try each direction in turn to find next clockwise boundary cell
            if dir == 'N':
                innerCell = (row, col+1)
                nextCell = (row-1, col)
            elif dir == 'E':
                innerCell = (row+1, col)
                nextCell = (row, col+1)
            elif dir == 'S':
                innerCell = (row, col-1)
                nextCell = (row+1, col)
            elif dir == 'W':
                innerCell = (row-1, col)
                nextCell = (row, col-1)
            if nextCell in boundary:
                direction = dir
                innerCells.append(innerCell)
                clockwise.append(nextCell) # will add the startCell at the end
                row, col = nextCell
                break

    for innerCell in innerCells:
        # floodfill empty cells from this inner cell, within boundary loop
        coordSet = floodfill(coordSet, innerCell, clockwise)
        # although all cells might be found in the first floodfill.. 
        # if the boundary walls touch, they may be separate areas to find, so test using all cells next to the boundary
            
    # return the number of squares filled
    # printGrid(coordSet)
    return len(coordSet)

def solveItPart1(instructions=testInstructions):
    # follow the instructions, digging a boundary around the lagoon then digging the enclosed cells
    # return the number of squares dug
    row, col = 0, 0
    boundary = []
    coordSet = set()
    for instruction in instructions:
        direction, spaces, color = instruction
        for i in range(int(spaces)):
            if direction == 'U':
                row -= 1
            elif direction == 'D':
                row += 1
            elif direction == 'L':
                col -= 1
            elif direction == 'R':
                col += 1
            # save the coordinates in a list
            boundary.append((row, col))
            # save the coordinates in a set
            coordSet.add((row, col))
    return countEnclosedCells(coordSet, boundary)

# Part 2 instructions now read differently: 
# 'colour' hexcode decoded to give the new directions and distances to move

def correctInstruction(instruction):
    _, _, code = instruction
    hexCode = code[2:-2] # remove outer brackets # and and final digit
    # Convert the first 5 digits of hexCode to decimal
    distance = int(hexCode, 16)  
    # Convert the final digit of hexCode to 'R', 'D', 'L', or 'U'
    final_digit = int(code[-2])
    if final_digit == 0:
        direction = 'R'
    elif final_digit == 1:
        direction = 'D'
    elif final_digit == 2:
        direction = 'L'
    elif final_digit == 3:
        direction = 'U'
    else:
        direction = None
    
    return (direction, distance)  # code wont be used again but third variable expected


def between(x, x1, x2):
    return x1 <= x <= x2 or x2 <= x <= x1

def inBetween(x, x1, x2):
    return x1 < x < x2 or x2 < x < x1

def adjacent(v1, v2, list):
    # test for adjacent values in a list, including the first and last values as adjacent indices
    if v1 not in list or v2 not in list:
        return False
    return list.index(v1) == list.index(v2)+1 or list.index(v1) == list.index(v2)-1 \
        or list.index(v1) == 0 and list.index(v2) == len(list)-1 

def getPairs(list):
    return [(list[i], list[i+1]) for i in range(len(list)-1)]

def sortedOnX(list):
    return sorted(list, key=lambda v: v[0])

def sortedOnY(list):
    return sorted(list, key=lambda v: v[1])

def openingsInWall(wall, boundary) :
    # returns the number of open cells (not on boundary) between vertices of a wall
    # assumes wall is horizontal
    (x1,y1), (x2,y2) = wall  
    level =  list(dict.fromkeys([wall[0]]+[(x,y) for (x,y) in boundary if y == y1]+[wall[1]])) # list(dict.fromkeys()) removes duplicates
    inWall = sortedOnX([(x,y) for (x,y) in level if between(x, x1, x2)]) 
    pairs = [p for p in getPairs(inWall)] 
    # openings are intervals in the wall that are not adjacent in the boundary
    openings = [p for p in pairs if not adjacent(p[0], p[1], boundary)]
    inOpening = [abs(x-x1)-1 for ((x,y),(x1,y1)) in openings]
    return sum(inOpening)

def openingsInVerticalWall(wall, boundary):
    # returns the number of open cells (not on boundary) between vertices of a verticalwall
    (x1, y1), (x2, y2) = wall
    level = list(dict.fromkeys([wall[0]] + [(x, y) for (x, y) in boundary if x == x1] + [wall[1]]))  # list(dict.fromkeys()) removes duplicates
    inWall = sortedOnY([(x, y) for (x, y) in level if between(y, y1, y2)])
    pairs = [p for p in getPairs(inWall)]
    # openings are intervals in the wall that are not adjacent in the boundary
    openings = [p for p in pairs if not adjacent(p[0], p[1], boundary)]
    inOpening = [abs(y - y1) - 1 for ((x, y), (x1, y1)) in openings]
    return sum(inOpening)

def hack(vertexList):
    # boundary is now large and can't be saved as a list of coordinates; use the
    # vertices of the boundary instead and calculate the enclosed area by hacking off
    # rectangles until the whole enclosed area is consumed.
    totalArea = 0
    # calculate the cells along the boundary edge, which are included in the area enclosed.
    if vertexList[0] == vertexList[-1]:
        vertexList = vertexList[:-1]
    b = [a for a in zip(vertexList, vertexList[1:]+[vertexList[0]])] 
    c = [abs(x2-x1)+abs(y2-y1) for (x1,y1),(x2,y2) in b]
    totalArea = totalArea + sum(c)

    vertexSet = set(vertexList)
    boundary = vertexList
    while len(vertexSet) > 0:
        # print(len(vertexSet))
        # sort vertices by x, then y
        vertexList = list(vertexSet)
        leftV = sorted(vertexList, key=lambda v: (v[0], v[1]))
        # make a box, cutting off the right end at the lowest x within the area of the for vertices
        # .. this could be bounded by other vertices between the top and bottom vertices
        # find vertices with y between y1 and y2 and smallest x
        alongRight = sorted([v for v in vertexSet if v[0] > leftV[0][0] and v[1] <= leftV[1][1] and v[1] >= leftV[0][1]], key=lambda v: v[0])
        x, _ = alongRight[0] # smallest x within the box 
        # toDo dont need sort.. can use min as only want first value
        _, y1 = leftV[0]
        _, y2 = leftV[1]
        rightV = [(x, y1), (x, y2)]
        box = [leftV[0], leftV[1], rightV[1], rightV[0]]
        # calculate the area of the box
        area = (abs(box[3][0] - box[0][0])-1) * (abs(box[0][1] - box[1][1])-1)
        add = openingsInVerticalWall((box[2], box[3]), boundary)
        totalArea = totalArea + area + add
        # remove the box boundary points and add in the box vertex that wasn't there before (if any),
        # new vertices are the ones in the box not already in the set
        new = set([v for v in box if v not in vertexSet])
        # remove the box vertices from the set, and add the new ones
        vertexSet.difference_update(box)
        vertexSet = vertexSet.union(new)
    return totalArea


def solveItPart2(instructions= testInstructions):
    # part 2 has much bigger lagoon area and too big to save coordinate lists.
    # instead, ??  save just the corners of the boundary...
    # fill between pairs of boundary walls in each row.

    revised = []
    for instruction in instructions:
        revised.append(correctInstruction(instruction))
    vertices = []
    position = (0,0)
    vertices.append(position)

    for instruction in revised:
        direction, spaces = instruction # test '_
        if direction == 'R':
            newPosition = (position[0]+spaces, position[1])
        elif direction == 'D':
            newPosition = (position[0], position[1]+spaces)
        elif direction == 'L':
            newPosition = (position[0]-spaces, position[1])
        elif direction == 'U':
            newPosition = (position[0], position[1]-spaces)
        
        vertices.append(newPosition)
        position = newPosition

    totalArea = hack(vertices)
    return totalArea

def rotate90Clockwise(pts):
    # rotate a list of points 90 degrees clockwise
    return [(-y, x) for (x,y) in pts]

def whittle(boundary) : 
    # Calculates the areas of an enclosed shape from its vertices on a grid.
    # Takes a list of vertices connected by horizontal or vertical lines
    
    # if the first and last vertices are the same, remove the last vertex
    # (the later rotation of the list relies on this)
    if boundary[0] == boundary[-1]:
        boundary = boundary[:-1]

    totalArea = 0
    # calculate the cells along the boundary edge, which are included in the area enclosed.
    b = [a for a in zip(boundary, boundary[1:]+[boundary[0]])] 
    c = [abs(x2-x1)+abs(y2-y1) for (x1,y1),(x2,y2) in b]
    totalArea = totalArea + sum(c)
    
    while len(boundary) > 3: 
        printLogGrid(boundary, True)

        # take a bite out of the top of the shape
        # find a pair of vertices at the top of the shape
        length = math.ceil(len(boundary)/4)
        minY = min([y for (x,y) in boundary])
        top = [(x,y) for x,y in boundary if y == minY]
        i = boundary.index(top[0]) # index of the first top vertex
        while i == 0 or i > len(boundary) - 3: # rotate the list until the top value is not at the start or end
            boundary = boundary[length:]+boundary[:length] # note this depends on end vertex not being same as first vertex
            i = boundary.index(top[0]) 
        # find vertices of an enclosed box with the top at the top of the shape
        below = [boundary[i-1][1], boundary[i+2][1]] 
        # base level is highest level of vertices in the box, below the top,
        # - could be level of an inner boundary, (as in the case of an inverted 'U' shape)
        for p in boundary :
            if inBetween(p[0], boundary[i-1][0], boundary[i+2][0]) and p[1] < min(below) :
                below.append(p[1]) 
        base = min(below)   
        box = [(boundary[i-1][0],base), boundary[i], boundary[i+1], (boundary[i+2][0],base)]
        new = [v for v in box if v not in boundary]
        if len(new) == 2: # there were vertices between the 1st and last box vertices 
            # rotate the shape and try again
            boundary = rotate90Clockwise(boundary)
            print('rotated')
            continue
        
        # calculate the number of cells enclosed by the box (excludes border cells) 
        area = (abs(box[3][0] - box[0][0])-1) * (abs(box[0][1] - box[1][1])-1)
        # add cells in the box bottom wall that are in openings in the boundary
        open = openingsInWall((box[0], box[3]), boundary)
        area = area + open
        totalArea = totalArea + area
        # remove the box boundary points and add in the box vertex that wasn't there before (if any),
        # to get the boundary of the remaining shape
        """         new = [v for v in box if v not in boundary]
        if len(new) == 2: # there were vertices between the 1st and last box vertices which must remain between the new ones
            boundary.insert(i+2, new[1])
            boundary.insert(i, new[0])
        else:  """
        boundary = boundary[:i] + new + boundary[i+2:]
        for v in box:
            if v in boundary:
                if v not in new:
                    boundary.remove(v)
    return totalArea
        

# find the topmost floor
def findTopmostFloor(walls):
    floors = [l for l in walls if l[0][1] == l[1][1]]
    top = min(f[0][1] for f in floors )
    topmost = [f for f in floors if f[0][1] == top]
    return topmost[0]

# find the area bounded on at the top by the topmost floor and sidewalls
def findTopArea(walls):
    topmost = findTopmostFloor(walls)
    # l is [start, end] where start is (x, y) and end is (x2, y2)
    walls = [l for l in walls if l[0][1] != l[1][1]]
    sidewalls = [w for w in walls if w[0] in topmost or w[1] in topmost]
    shortest = min(w[0][1] for w in sidewalls)
    # s = min(y,y1) for [(x,y)(x1,y1)] in sidewalls)
    # newWall = 
    #print(sidewalls)



with open('day18_input.txt', 'r') as file:
    instructions = [(direction, spaces, color) for 
        (direction, spaces, color) in [line.split(' ') for line in file.read().splitlines()]] 
    
print('Part 1: ', solveItPart1(instructions)) # 39194

print('Part 2: ', solveItPart2(instructions)) # 78242031808225



