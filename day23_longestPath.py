# Find the longest path through a maze, from a start point to a finish point. 
# Part 1 restricts certain moves away from junctions, reducing the size of the search.
# Part 2 allows any move, with many more routes.
# I found the recursive, recursive, DFS slower than the stack-based BFS. 
# The BFS also solved Part 2 in a resonable time, the DFS did not finish.


testData = [
'#.#####################',
'#.......#########...###',
'#######.#########.#.###',
'###.....#.>.>.###.#.###',
'###v#####.#v#.###.#.###',
'###.>...#.#.#.....#...#',
'###v###.#.#.#########.#',
'###...#.#.#.......#...#',
'#####.#.#.#######.#.###',
'#.....#.#.#.......#...#',
'#.#####.#.#.#########v#',
'#.#...#...#...###...>.#',
'#.#.#v#######v###.###v#',
'#...#.>.#...>.>.#.###.#',
'#####v#.#.###v#.#.###.#',
'#.....#...#...#.#.#...#',
'#.#########.###.#.#.###',
'#...###...#...#...#.###',
'###.###.#.###v#####v###',
'#...#...#.#.>.>.#.>.###',
'#.###.###.#.###.#.#v###',
'#.....###...###...#...#',
'#####################.#',
]

testGrid = [list(line) for line in testData]
testTarget = (len(testGrid[0])-2, len(testGrid)-1)

def printSet(grid, s):
    print('length ',len(s))
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x,y) in s:
                print('O', end='')
            else:
                print(grid[y][x], end='')
        print()

def getNeighbours(position, grid):
    # return neighbouring cells that are not walls ('#')
    neighbours = []
    if position[0] > 0:
        neighbours.append((position[0]-1, position[1]))
    if position[0] < len(grid[0])-1:
        neighbours.append((position[0]+1, position[1]))
    if position[1] > 0:
        neighbours.append((position[0], position[1]-1))
    if position[1] < len(grid)-1:
        neighbours.append((position[0], position[1]+1))
    return [n for n in neighbours if grid[n[1]][n[0]] != '#']

def getChoices(position, grid):
    # get path choices - neighbouring positions that are not walls
    # if the position contains an arrow, the next position is the one in the direction of the arrow
    if grid[position[1]][position[0]] == '>':
        choices = [(position[0]+1, position[1])]
    elif grid[position[1]][position[0]] == '<':
        choices = [(position[0]-1, position[1])]
    elif grid[position[1]][position[0]] == '^':
        choices = [(position[0], position[1]-1)]
    elif grid[position[1]][position[0]] == 'v':
        choices = [(position[0], position[1]+1)]
    else:
        choices = [n for n in getNeighbours(position, grid)]
    return choices

def longestPath(position=(1, 0), path_length = 0, grid=testGrid, end=testTarget, visited=set()):

    if position == end:
        printSet(grid, visited)
        return path_length # last step tasklen.  Will wind back up, returning the longest path from the base case
    if position in visited:
        return 0  # dead end or going backwards; must not go over a position twice so not a route
    visited.add(position)
    if len(visited) > 0 and len(visited) % 100 == 0:
        printSet(grid,visited)

    choices = getChoices(position, grid)  
    longest_length = 0
    for choice in choices:
        result = longestPath(choice, path_length+1, grid, end, visited.copy())
        if result:
            longest_length = max(result, longest_length)

    return longest_length 

def longestPath2(position=(1, 0), path_length=0, grid=testGrid, end=testTarget, visited=set()):
# Interesting that this is the better solution.. faster, simpler to understand too.  Should consider stacks more!

    stack = [(position, path_length, visited)]
    longest_length = 0

    while stack:
        position, path_length, visited = stack.pop()
        
        if position == end:
            #printSet(grid, visited)
            longest_length = max(longest_length, path_length)
            continue
        
        if position in visited:
            continue  

        visited.add(position)
        choices = getChoices(position, grid) 

        for choice in choices:
            stack.append((choice, path_length + 1, visited.copy())) # note that need to remember the visited set reached at this point, to return to
    return longest_length


def longestPart2Stack(junction, adjacencyMatrix, end=testTarget, visited=set()):
    # This BFS approach did solve Part 2. 

    stack = [(junction, 0, visited)]
    longest_length = 0

    while stack:
        junction, path_length, visited = stack.pop()
        
        if junction == end:
            longest_length = max(longest_length, path_length)
            continue
        
        visited.add(junction)
        choices = adjacencyMatrix[junction]

        for choice in choices:
            if choice in visited:
                continue
            segment_length = adjacencyMatrix[junction][choice] + 1
            stack.append((choice, path_length + segment_length, visited.copy())) # note that need to remember the visited set reached at this point, to return to

    return longest_length


def getAdjacencyMatrix(start, target, grid):
    #return a directory of directories of the junctions with their neighbouring junctions and path length between them
    adjacencyMatrix = {}
    visited = set()
    q = [start]
    gridPoints = [(x, y) for y in range(len(grid)) for x in range(len(grid[0])) if grid[y][x] == '.']
    junctions = [(x,y) for (x,y) in gridPoints if len(getNeighbours((x,y), grid)) > 2]
    junctions.append(target)
    junctions.append(start)
    # initialise adjacency matrix for all pairs of junctions to 0 
    for j in junctions:
        adjacencyMatrix[j] = {}
    """         for j2 in junctions:  # not needed cept for floyd-warshall
            adjacencyMatrix[j][j2] = 0 """
    
    while len(q) > 0:
        junction = q.pop()
        visited.add(junction)
        if junction not in adjacencyMatrix:
            adjacencyMatrix[junction] = {}
        choices = getNeighbours(junction, grid)  # any neighbours that are not walls

        for position in choices: # move in each direction away from the junction
            if position in visited:
                continue
            path_length = 0
            while position not in junctions:
                path_length += 1
                visited.add(position)
                position = [n for n in getNeighbours(position,grid) if n not in visited][0]

            # position is a junction -  add path length to adjacency matrix
            adjacencyMatrix[junction][position] = path_length
            if position not in adjacencyMatrix:
                adjacencyMatrix[position] = {}
            adjacencyMatrix[position][junction] = path_length  # undirected graph
            q.append(position)

    return adjacencyMatrix

def getDistanceMatrix(adjacencyMatrix):
    # use -ve weights for distances.
    sign =-1
    distanceMatrix = {}
    for key in adjacencyMatrix.keys():
        distanceMatrix[key] = {}

    for node in adjacencyMatrix:
        # distanceMatrix[node] = {}
        for node2 in adjacencyMatrix:
            if node == node2:
                distanceMatrix[node][node2] = sign * float('inf') #normally, for shortest path, 0
            elif adjacencyMatrix[node][node2] == 0: 
                distanceMatrix[node][node2] = float('inf')
            else:
                distanceMatrix[node][node2] = sign * adjacencyMatrix[node][node2]
    return distanceMatrix

def floydWarshall(distanceMatrix):
    # return the longest distance between all pairs of nodes (> instead of < for longest, and negative weight distances)
    nodes = list(distanceMatrix.keys())
    for k in nodes:
        for i in nodes:
            for j in nodes:
                if i == k or j == k: # added this 
                    continue
                if distanceMatrix[i][k] + distanceMatrix[k][j] < distanceMatrix[i][j]:
                    distanceMatrix[i][j] = distanceMatrix[i][k] + distanceMatrix[k][j]
    return distanceMatrix
                    

def longestPart2(junction, adjacencyMatrix, end, visited=set(), memo = {}):
    
    if junction in visited: 
        return None  # cannot revisit a cell
    visited.add(junction)
  
    stringVisited = ''.join(str(e) for e in sorted(list(visited)))  # sorted because order of visited cells does not matter; key will be the same
    key = (junction, stringVisited)  # memoization key
    if key in memo:
        return memo[key]

    if junction == end:
            return 0 # base case. last step taken.  Will wind back up, returning the longest path from the base case

    nexts = adjacencyMatrix[junction]
    longest_length = 0
    for next in nexts:
        result = longestPart2(next, adjacencyMatrix, end, visited.copy(), memo)
        if result != None:
            path_length = 1 + result + adjacencyMatrix[junction][next]
            if path_length > longest_length:
                longest_length = path_length
   
    memo[key] = longest_length # memoise the result
    return longest_length 

def readInputFile(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
        grid = [list(line.strip()) for line in lines]
    return grid

grid = readInputFile('day23_input.txt')
start = (1,0)
target = (len(grid[0])-2, len(grid)-1)

def solveItPart2(start, target, grid):
    adjacentMatrix = getAdjacencyMatrix(start, target, grid)

    # return longestPart2(start, adjacentMatrix, target) # This (DFS) never solved part 2 (ran for many minutes not solved)
    # Is the DFS stuck in a cycle? 
    return longestPart2Stack(start, adjacentMatrix, target) # 6322 .. but this did; BFS
    
    # also tried floyd-Warshall algorithm wth -ve weights - but did not get right answer
     # distanceMatrix = getDistanceMatrix(adjacentMatrix)
    # longestPaths = floydWarshall(distanceMatrix)
    # givews 1334.   ..cannot be less than 2114 (part 1 answer) or more than 9xxx the numner of grid points

print('Part 1', longestPath(start, 0, grid, target)) # 2114
print('Part 2: ', solveItPart2(start, target, grid)) # 6322





