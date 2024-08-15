"""Find the number of garden plots that can be reached by making an exact number of steps from a starting point
into open plots on a grid (marked '.').  Part 1 the number of steps is 64.  In part 2 the grid repeats infinitely and the 
number of steps is 26501365
Plots reached at an even step can always be reached again at the next even steps, (by going back).
- Used this in Part 2 to calculate the filled cells at odd and even sets, as previously filled cells
plus newly reached cells with a neighbour in the last (odd or even) step set.
Part 2 solution required the filled cells at the required step number to be calculated from a
pattern establishes over repeating grids.   """  

testData = [
'...........',
'.....###.#.',
'.###.##..#.',
'..#.#...#..',
'....#.#....',
'.##..S####.',
'.##..#...#.',
'.......##..',
'.##.#.####.',
'.##..##.##.',
'...........',
]

import math

# read test data into a grid
testGrid = []
for line in testData:
  testGrid.append(list(line))

# read input file into a grid
with open('day21_input.txt', 'r') as file:
    lines = file.read().splitlines()

grid = []
for line in lines:
    grid.append(list(line))
  
# print the grid, replacing values in the set filled_set with symbol 'O
def printGrid(grid, filled_set, sym = 'O'):
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if (x, y) in filled_set:
        print(sym, end='')
      else:
        print(grid[y][x], end='')
    print()

def getStart(grid):
  # find the starting point
  for y in range(len(grid)):
    for x in range(len(grid[y])):
      if grid[y][x] == 'S':
        return (x, y)

def solveItPart1(grid, steps):
    # add the starting space to a set of garden plots 'plots'
    plots = set()
    start = getStart(grid)
    plots.add(start)
    # Find the empty spaces one step away in a direction <>^v if the next step is a . or S
    for step in range(steps): # find the plots reached at exactly steps number
        oneStep = set()
        newPlots = set()
        for plot in plots:
            x, y = plot
            for direction in [(0,1), (0,-1), (1,0), (-1,0)]:
                dx, dy = direction
                if 0 <= x+dx < len(grid[0]) and 0 <= y+dy < len(grid) and grid[y+dy][x+dx] in '.S':
                    oneStep.add((x+dx, y+dy))
        # newPlots = oneStep.difference(plots)
        # printGrid(grid, newPlots)
        plots = oneStep.copy()
    printGrid(grid, plots)
    return len(plots)

print('Part 1 : ', solveItPart1(grid, 64)) #64 steps  3743

def infiniteGrid(point, grid):
    # grid repeats infinitely in all directions
    # return the value of the grid at point
    x, y = point
    return grid[y % len(grid)][x % len(grid[0])]

def getneighbours(x,y):
    # return the 4 neighbours of a point
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def getNewlyReachedPlots(step, grid, start):
  # newly reached cells have x-startx + y-starty = step
  start_x, start_y = start
  newPlots = set()
  for x in range(step+1) :
    y = step - x
    newPlots.add((start_x + x, start_y + y))
    newPlots.add((start_x - x, start_y + y))
    newPlots.add((start_x + x, start_y - y))
    newPlots.add((start_x - x, start_y - y))
  return {p for p in newPlots if infiniteGrid(p, grid) in '.S'} # only open cells included

def openNeighbours(x, y, grid):
  # return the set of open neighbours of a point
  neighbours = set()
  for next in getneighbours(x, y):
    if infiniteGrid(next, grid) in '.S':
      neighbours.add(next)
  return neighbours
                
def intervals(arr) :
   # return an array of the intervals between the elements of arr
    return [arr[i+1] - arr[i] for i in range(len(arr)-1)]

def extendByCalculation(steps, filledDict, saveFilled):
  # add additional entries to the filledDict by calculation, following pattern of entries at repeating grid intervals
  gaps = intervals(saveFilled) # interval between filledDict entries
  gapsInGaps = intervals(gaps) # interval between intervals - becomes constant

  keys = [k for k in filledDict.keys()]
  keyInterval = keys[len(keys)-1] - keys[len(keys)-2] # further intervals will be constant
  lastKey = keys[len(keys)-1]
  nextKey = lastKey + keyInterval
  constant = gapsInGaps[len(gapsInGaps)-1] # interval between intervals become constant after [2] repeats
  gap = gaps[len(gaps)-1] # interval between filledDict entries becomes constant after [2] repeats
  while nextKey <= steps:
    gap += constant # extend gap by adding the constant interval
    filledDict[nextKey] = filledDict[lastKey] + gap  # extend the filledDict array using the calculated gap
    lastKey = nextKey
    nextKey = nextKey + keyInterval
  return filledDict

def solveItPart2(grid=testGrid, steps=500) : 
  start=getStart(grid)
  evenFilled = set()
  evenFilled.add(start) # the start cell is filled at step 0
  oddFilled = set() 
  evenUnfilled = set()
  oddUnfilled = set()
  remainder = steps % len(grid) 
  saveEvenFilled = []
  saveOddFilled = []
  evenDict = {}
  oddDict = {}
  for step in range(1,steps+1):  # first step will be 1
    newlyReached = getNewlyReachedPlots(step, grid, start) # These are cells on the perimeter of the shape reached
    if step % 2 != 0: # an oddnumbered step
      # any empty cells reached which have neighbours in the filled even set will now be filled.
      unfilled = newlyReached.union(oddUnfilled)
      newlyFilled = {p for p in unfilled if len(openNeighbours(p[0], p[1], grid).intersection(evenFilled)) > 0}
      oddFilled = oddFilled.union(newlyFilled)
      oddUnfilled = unfilled.difference(newlyFilled)
    else: # an even numbered step
      # any empty cells reached which have neighbours in the filled odd set will now be filled.
      unfilled = newlyReached.union(evenUnfilled)
      newlyFilled = {p for p in unfilled if len(openNeighbours(p[0], p[1], grid).intersection(oddFilled)) > 0}
      evenFilled = evenFilled.union(newlyFilled)
      evenUnfilled = unfilled.difference(newlyFilled)
    # N.B. if needed could reduce memory by only storing filled cell corrdinates where they have unfilled neighbours
    
    if (step - remainder) % len(grid) == 0:  # these are intervals that reach the required step number at repeating grid pattern intervals
      if step % 2 == 0:
        evenDict[step] = len(evenFilled)
        saveEvenFilled.append(len(evenFilled)) 
      # stop after some repeats
        if len(saveEvenFilled) > 4:
          break
      else:
        oddDict[step] = len(oddFilled)
        saveOddFilled.append(len(oddFilled))
      # stop after some repeats
        if len(saveOddFilled) > 4:
          break

  if steps % 2 == 0:
    if step < steps:
      evenDict = extendByCalculation(steps, evenDict, saveEvenFilled)
    return evenDict[steps]
  else:
    if step < steps:
      oddDict = extendByCalculation(steps, oddDict, saveOddFilled)
    return oddDict[steps]
   
   

       

print('Part 2 :', solveItPart2(grid, 26501365)) # 618261433219147 
  

