testData = [
'19, 13, 30 @ -2,  1, -2',
'18, 19, 22 @ -1, -1, -2',
'20, 25, 34 @ -2, -2, -4',
'12, 31, 28 @ -1, -2, -1',
'20, 19, 15 @  1, -5, -3',
]

data = testData
testArea =[(7,7),(27,27)]

with open('day24_input.txt', 'r') as file:
    data = file.read().splitlines()

testArea = [(200000000000000,200000000000000),(400000000000000,400000000000000)]

lineList = []
for line in range(len(data)):
    p, v = data[line].split('@')
    x,y,z = p.split(',')
    vx, vy, vz = v.split(',')
    lineList.append([[int(x),int(y)], [int(x)+int(vx),int(y)+int(vy)]])


""" The point of intersection formula is used to find the point of intersection of the two lines, that is the meeting point of two lines. ...
a1x+b1y+c1=0 and a2x+b2y+c2=0.
x= (b1c2-b2c1)/(a1b2-a2b1)
y=(c1a2-c2a1)/(a1b2-a2b1)
(x, y) = ((b1c2-b2c1)/(a1b2-a2b1), (c1a2-c2a1)/(a1b2-a2b1)) """

def intersection(p1, p2, p3, p4):
    # return the intersection point of two lines
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    a1 = y2 - y1
    b1 = x1 - x2
    c1 = a1 * x1 + b1 * y1
    
    a2 = y4 - y3
    b2 = x3 - x4
    c2 = a2 * x3 + b2 * y3
    
    determinant = a1 * b2 - a2 * b1
    
    if determinant == 0:
        return None
    else:
        x = (b2 * c1 - b1 * c2) / determinant
        y = (a1 * c2 - a2 * c1) / determinant
        return (x, y)


intersectionCount = 0
for i, line in enumerate(lineList):
    print(i)
    for line2 in lineList[i+1:] :
        p1, p2 = line
        p3, p4 = line2
        if intersection(p1, p2, p3, p4) is not None:
            x, y = intersection(p1, p2, p3, p4)
            # for collision, both hailstones must reach the intersection at the same time, in the future
            vx1 = p2[0] - p1[0]
            vx2 = p4[0] - p3[0] 
            n = (x - p1[0]) / vx1
            m = (x - p3[0]) / vx2
            if n > 0 and m > 0: # for a collison, n would also be equal to m
                print(x-testArea[0][0], x-testArea[1][0], y-testArea[0][1], y-testArea[1][1])
                print(x>=testArea[0][0], x<=testArea[1][0], y>=testArea[0][1], y<=testArea[1][1])
                if x >= testArea[0][0] and x <= testArea[1][0] and y >= testArea[0][1] and y <= testArea[1][1]:
                    intersectionCount += 1
                    print(x, y, line, line2)
 
print(intersectionCount)