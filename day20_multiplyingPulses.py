"""When a button is pressed, a low pulse is sent to the the broadcaster module, which sends sends pulses to each module in its list.
Those modules send high or low or no pulses to each module in their list or to output, and so on, until all pulses are handled.

There are 3 different types of modules: flipflops, conjunctions, and the broadcaster.
1) Flipflops (%) are initially off. If a flip-flop recieves a high pulse; nothing happens.
If a flip-flop recieves a low pulse, it changes state (from on to off or off to on) and sends a high pulse.
2) Conjunctions (&) remember the last pulse recieved from each of their input modules; initially 
remembering low.  When a pulse is recieved, the conjuncton first updates its memory for that input,
then, if it remembers high pulses for all inputs, it sends a low pulse, otherwise it sends a high pulse.
3) The single broadcaster module sends the same pulse as it recieves, to all modules in its list.

Pulses are always processed in the order they are sent (pulses sent to a, b and c, then b would be handled
before any pulses sent by a.)

Part 1: Count the number of high passes and the number of low passes sent in 1000 button
presses. Return the product of the two counts.

Part 2: Find the smallest number of button presses to transmit a single low pulse to module 'rx'
This required finding the cycles at which the inputs to the conjunction module cl are high when they fire
and calculation of the lowest common multiple of the intervals between these cycles"""
import queue
import re
import math

testData = [
'broadcaster -> a',
'%a -> inv, con',
'&inv -> b',
'%b -> con',
'&con -> output',
]
# test data formatted for use as follows:
# broadcastTo = ['a']
# flipFlops = {'a': ['inv', 'con'], 'b': ['con']}
# conjunctions = {'inv': ['b'], 'con': ['output']}

with open('day20_input.txt', 'r') as file:
  lines = file.read().splitlines()

ffsRegex =re.compile(r'%(\w+) -> (\w+)')
broadcastToRegex = re.compile(r'broadcaster -> (\w+)')
conjunctionsRegex = re.compile(r'&(\w+) -> (\w+), (\w+)')

def processInputData(lines):
  flipFlops = {}
  broadcastTo = []
  conjunctions = {}
  for line in lines:
    code, values = line.split(' -> ') 
    if code == 'broadcaster':
      broadcastTo += [value.strip() for value in values.split(',')]
    elif code[0] == '%':
      flipFlops[code[1:]] = [value.strip() for value in values.split(',')]
    elif code[0] == '&':
      conjunctions[code[1:]] = [value.strip() for value in values.split(',')]
  
  return (flipFlops, broadcastTo, conjunctions)

# Used classes for module types .. helps to remember state of each module after pulse sent to it
class flipFlop:
  def __init__(self):
    self.status = 'off'
   
  def flip_status(self):
    if self.status == 'off':
        self.status = 'on'
        return 'high'
    else:
        self.status = 'off'
        return 'low'
      
  def pulseIn(self, pulse):
      if pulse == 'low':
        return self.flip_status()
      return 0 # No pulse returned
    
class conjunction():
  def __init__(self, inputModules):
    self.pulseMemory = {}
    # Each conjunction module remembers the last pulse (high or low) last sent from an input module; intialised as 'low'
    for module in inputModules:
        self.pulseMemory[module] = 'low'

  def pulseIn(self, inpModule, pulse):
    self.pulseMemory[inpModule] = pulse
    test = [v == 'high' for v in self.pulseMemory.values()]
    if all(test):
       return 'low'
    else:
       return 'high'


def getConjunctionInputs(flipFlops, broadcastTo, conjunctions) :
  # find all the input modules for conjunctions
  # initialse the flipflops and conjunctions
  conjunctionInputs = {}

  for c in conjunctions.keys():
    conjunctionInputs[c] = []  # conjunctionInputs is a dictionary of lists of input modules for each conjunction
  for ff in flipFlops.keys():
    for output in flipFlops[ff] :
      if output in conjunctions.keys():  
        conjunctionInputs[output].append(ff)  #..this ff outputs to a conjuction 

  for output in broadcastTo:
    if output in conjunctions.keys():
      conjunctionInputs[output].append('broadcast')  #..the broadcaster outputs to a conjuction
  for c in conjunctions.keys():
    for output in conjunctions[c] :
      if output in conjunctions.keys():  
        conjunctionInputs[output].append(c)  #..this conjunction outputs to a conjuction


  return (conjunctionInputs)

def transmit(inputModule, pulse, outputModules, q):
  for module in outputModules:
    q.put((inputModule, module, pulse))
  return q

def solveItPart1() : 
  (flipFlops, broadcastTo, conjunctions) = processInputData(lines)
  # initialise dictionaries of flipflops and conjunction objects
  conjunctionInputs = getConjunctionInputs(flipFlops, broadcastTo, conjunctions)
  ffDict = {}
  cDict = {}
  for ff in flipFlops.keys():
    ffDict[ff] = flipFlop()
  for c in conjunctionInputs.keys():
    cDict[c] = conjunction(conjunctionInputs[c])

  pulseCount = {'low':0 ,'high':0}
  buttonPresses = 1000
  for button in range(buttonPresses) :
    q = queue.Queue()
    pulse = 'low'
    pulseCount[pulse] = pulseCount[pulse] + 1 # buttonpress pulse
    q = transmit('broadcaster', pulse, broadcastTo, q)
    pulseCount[pulse] = pulseCount[pulse] + len(broadcastTo) # broadcast pulses
    while not q.empty() :
      inputModule, module, pulse = q.get()
      # print(inputModule, module, pulse)
      # send the pulse to this module and get the next pulse
      if module in ffDict.keys(): 
        pulse = ffDict[module].pulseIn(pulse)
        if pulse != 0: # !! There may be no pulse returned from a flipflop
          q = transmit(module, pulse, flipFlops[module], q)
          pulseCount[pulse] = pulseCount[pulse] + len(flipFlops[module]) # flipflop pulses
      elif module in cDict.keys():
        pulse = cDict[module].pulseIn(inputModule, pulse)
        q = transmit(module, pulse, conjunctions[module], q)
        pulseCount[pulse] = pulseCount[pulse] + len(conjunctions[module]) # conjunction pulses
  return(pulseCount['low']*pulseCount['high']) # 938065580


# Part 2.  Smallest number of button presses to transmit a single low pulse to module 'rx'
# This occurs when low pulse is sent from conjunction cl, which happends when
# all the flipflops or conjunctions sending to cl are in 'high' state, and one of the modules sending to cl sends to it
# Several conjunctors send to cl.
# ... Find the cycles at which a module sends to cl, and the cycles at which all the flipflops/cs sending to cl are high
# looking for repeat patterns in the cycles

# flipflops change state when a low pulse is sent to them, so check after a low pulse is sent.
# button presses result in a number of pulses being sent.. changes. 
# Need pulse sent to cl and all flipflops sending to cl high
# Track pulses per buttonpress, pulses where cl receives a pulse, pulses where all flipflops sending to cl are high

def checkClInputsHigh(lastRecordedPulse):
  # check whether lastrecordedpulse for all inputs to cl is high
  return all([v == 'high' for v in lastRecordedPulse.values()])

def solveItPart2(lines) :
  (flipFlops, broadcastTo, conjunctions) = processInputData(lines)
  conjunctionInputs = getConjunctionInputs(flipFlops, broadcastTo, conjunctions)
  ffDict = {}
  cDict = {}
  for ff in flipFlops.keys():
    ffDict[ff] = flipFlop()

  for c in conjunctions.keys():
    # cDict[c] = conjunction(c) # cDict is a dictionary of conjunction objects  !! check this - newly addee
    cDict[c] = conjunction(conjunctionInputs[c]) # cDict is a dictionary of conjunction objects
  # find the smallest number of button presses to transmit a single low pulse to module 'rx'
  # ..conjunction module cl will send a low pulse to 'rx' when all its inputs are remembered as high
  pulseNumber = 0
  pulseCount = {'low':0 ,'high':0}
  buttonPresses = 10000

  clInputsDict = {} # prepare a dictionary to record when inputs to cl fire (cl fires to rx.)
  lastRecordedPulse = {} # prepare a dictionary to record last pulse sent to cl that differed from the previous one.
  clInputsHighButtonpress = {} # prepare a dictionary to record the button press in which a high pulse was recieved
  clInputsButtonInterval = {} # prepare a dictionary to record the interval between buttob presses where a high pulse was sent

  for module in conjunctionInputs['cl']:
    clInputsDict[module] = {'low':[], 'high':[]} # will record pulse number for pulse type when it fires 
    lastRecordedPulse[module] = 'low'
    clInputsHighButtonpress[module] = [] 
    clInputsButtonInterval[module] = []

  for button in range(buttonPresses) :
    q = queue.Queue()
    pulse = 'low'
    pulseCount[pulse] = pulseCount[pulse] + 1
    q = transmit('broadcaster', pulse, broadcastTo, q)
    pulseCount[pulse] = pulseCount[pulse] + len(broadcastTo)
    while not q.empty():
      inputModule, module, pulse = q.get()
      if module == 'cl': 
        if pulse == 'high' and lastRecordedPulse[inputModule] == 'low' :
          # switching to high (on) from low (off)
          lastRecordedPulse[inputModule] = 'high' 
          clInputsHighButtonpress[inputModule].append(button)
          # check whether lastrecordedpulse for all inputs to cl is high - the answewr has been found
          if checkClInputsHigh(lastRecordedPulse):
            print("!!!! pulse number, buttonPress", pulseNumber, button)
        elif pulse == 'low' and lastRecordedPulse[inputModule] == 'high' :
          # switching to low (off) from high (on)
          lastRecordedPulse[inputModule] = 'low' 
      if module in ffDict.keys(): # There may be no pulse returned
        pulse = ffDict[module].pulseIn(pulse)
        if pulse != 0:
          q = transmit(module, pulse, flipFlops[module], q)
          pulseCount[pulse] = pulseCount[pulse] + len(flipFlops[module])
      elif module in cDict.keys():
        pulse = cDict[module].pulseIn(inputModule, pulse)
        q = transmit(module, pulse, conjunctions[module], q)
        pulseCount[pulse] = pulseCount[pulse] + len(conjunctions[module])
  # check that high and low button pulses switching on/off are in the same button press - Not needed

  # find the interval between button presses where a high pulse was sent by each input module to cl        
  buttonIntervals = []
  for k in clInputsDict.keys():
    for i in range(1,len(clInputsHighButtonpress[k])):
      clInputsButtonInterval[k].append(clInputsHighButtonpress[k][i]-clInputsHighButtonpress[k][i-1])
  # .. above (at larger buttonpress number) confirmed that intervals are contant for each input module
  # find the lcm of the constant intervals..  
    buttonIntervals.append(clInputsButtonInterval[k][0])
  return(math.lcm(*buttonIntervals)) 
  
# print('Part 1 :', solveItPart1())
print('Part 2 :', solveItPart2(lines)) # 250628960065793

# move ff into a subroutine. document