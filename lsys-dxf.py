import sys
import math
import operator
import sdxf

infile = sys.argv[1]
f = open(infile)
depth = int(f.readline()[:-1])
angle = float(f.readline()[:-1])
print angle
axiom = f.readline()[:-1]
print axiom
rules = f.readline()[:].split(', ')
print rules
ruleDict = {}
for rule in rules[:]:
    rule = rule.split('=')
    ruleDict[rule[0]] = rule[1]
print ruleDict

x = 0
y = 1
theta = 2

stack = []
length = 2**-depth
pos = [0,0,0]
d=sdxf.Drawing()
def drawForward():
    global pos
    newPos = map(operator.add, pos,
                 [length*math.cos(math.radians(pos[theta])),
                  length*math.sin(math.radians(pos[theta])), 0])
    d.append(sdxf.Line(points=[pos,newPos]))
    pos = newPos

def goForward():
    global pos
    pos = map(operator.add, pos,
              [length*math.cos(math.radians(pos[theta])),
               length*math.sin(math.radians(pos[theta])), 0])

def turnRight():
    global pos
    pos[theta] = (pos[theta] - angle) % 360

def turnLeft():
    global pos
    pos[theta] = (pos[theta] + angle) % 360

def push():
    global pos
    #pass by reference, tricksy tricksy, hence slice copy
    stack.append(pos[:])
    print "push", stack

def pop():
    global pos
    print "pop", pos, stack
    pos = stack.pop()
    print "pop", pos

def moveLength():
    global pos
    pass

commandDict = {'F': drawForward,
               'G': goForward,
               '+': turnRight,
               '-': turnLeft,
               '[': push,
               ']': pop,
               '|': moveLength
               }

#print axiom
for i in range(depth):
    outstr = ''
    for char in axiom:
        if char in ruleDict.keys():
            outstr += ruleDict[char]
        else:
            outstr += char
    axiom = outstr
#    print axiom

print axiom
for char in axiom:
#    print char, pos
    try:
        commandDict[char]()
    except KeyError:
        pass
d.saveas('test.dxf')
