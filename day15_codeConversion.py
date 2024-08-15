"""Follow instructions to add, replace or remove lenses to slots in boxes"""


testInput = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'

def HashAlgorithm(input='HASH'):
    v = 0
    # for each input character
    for c in input:
        # step 1: get ASCII value 
        v += ord(c)
    # step 2: multiply by 17
        v *= 17
    # step 3: mod by 256
        v %= 256
    return v

# HashAlgorithm('rn=1')

def solveItPart1(instructions=testInput.split(',')):
    # add the values of HashAlgoritm(instruction) for each input instruection
    return sum([HashAlgorithm(instruction) for instruction in instructions])

# print('Part 1 test: ', solveItPart2())
print('Part 1: ', solveItPart1(open('day15_input.txt', 'r').read().split(','))) # 259333

def addOrReplace(boxes, box_number, label, focal_length):
    # for this box_number in boxes, if the list contains a lens (label, focal_length) with this label
    # replace the focal_length of this lens with the new focal_length.
    # else add (label, focal_length) to the list

    for i, (l, f) in enumerate(boxes[box_number]):
        if l == label:
            del boxes[box_number][i]
            boxes[box_number].insert(i, (label, focal_length))
            return boxes
    boxes[box_number].append((label, focal_length)) # lens label not found; add to end of list
    return boxes

def remove(boxes, box_number, label):
    # for this box_number in boxes, if the list contains a lens (label, focal_length) with this label
    # remove the lens from the list
    for i, (l, f) in enumerate(boxes[box_number]):
        if l == label:
            del boxes[box_number][i]
            break
    return boxes


def calcFocusingPower(boxes):
    # focussing power is the sum for each lens in the boxes of
    # (box number + 1) * (slot number + 1) * (focal length)
    # where box number is the key of the dictionary
    fp = 0
    for box in boxes.keys():
        for slot, (_, focal_length) in enumerate(boxes.get(box)):
            fp += (box + 1) * (slot + 1) * int(focal_length)
    return fp

def solveItPart2(instructions=testInput.split(',')):
    # create a dictionary of lists with keys 0 to 255, each list is empty
    boxes = {key: [] for key in range(256)}

    # follow instructions to add and remove items from the lists
    for instruction in instructions:
        if '=' in instruction:
            label, focal_length = instruction.split('=')
            box_number = HashAlgorithm(label)
            boxes = addOrReplace(boxes, box_number, label, focal_length)
        elif '-' in instruction:
            label = instruction[:-1]
            box_number = HashAlgorithm(label)
            boxes = remove(boxes, box_number, label)

    return calcFocusingPower(boxes)

# print('Part 2 test: ', solveItPart2())
print('Part 2: ', solveItPart2(open('day15_input.txt', 'r').read().split(','))) # 259333


