
# Victor Phillips CSCE 355
# Choice # 5
# Inverse Homomorphic Image
from collections import OrderedDict
import re
import sys
import string

# Global Variables
# Mostly attributes belonging to DFAs
dfa = OrderedDict()
trans = []
DFA_desc = []
F = []
E = []
Q = ''
inputStrings = ''

def fillDictionary():
    #print("fillDict")
    # Filling the dictionary with states and transitions
    global Q
    global E
    global dfa
    for a in range(Q):
        dfa[a] = OrderedDict()
        for b in E:
            dfa[a][b] = ''

def assignValues():
    #print("assignV")
    # Getting the junk out of DFA_desc inputfile
    global Q
    global DFA_desc
    global F
    global E
    global dfa
    skippableChars = 10

    Q = int(re.sub("\D", "", DFA_desc[0]))

    F = int(re.sub("\D", "", DFA_desc[1]))
    F = [int(d) for d in str(F)]

    E  = [a for a in DFA_desc[2][skippableChars:]]
    fillDictionary()

def transTable():
    #print("table")
    # Everything from the 4th line down should only be the transition Table
    global trans
    global DFA_desc
    trans = [a for a in DFA_desc[3:]]
    for a in range(len(trans)):
        trans[a] = re.findall('\d+', trans[a])

def assignStates():
    #print("assignStates")
    global dfa
    global trans
    global E
    for states in dfa:
        for y, x in enumerate(dfa[states]):
            for z in range(len(E)):
                dfa[states][x] = trans[states][y]

def loopThrough():
    #print if the strings are accepted or not
    global inputStrings
    global F
    try:
        for i in inputStrings:
            state = '0'
            for j in i:
                state = dfa[int(state)][j]
            if int(state) in F:
                print("accepted")
            elif int(state) not in F:
                print("rejected")
    except Exception as error:
        print("Error thrown at: ", error)

def readDFA():
    #print("readDFA")
    global F
    global DFA_desc
    global dfa
    # reading the file into a variable I can manipulate
    DFA_desc = [read.rstrip('\n') for read in open(sys.argv[1])]
    #dictTest()
    assignValues()
    transTable()
    assignStates()

def applyStrings():
    # Checks if the given DFA accepts the given strings
    global inputStrings
    try: #strips the string of un-needed chars
        inputStrings = [read.rstrip('\n') for read in open(sys.argv[2])]
    except Exception as error:
        print("Please provide a file of strings to test")
    loopThrough()

def simHomo():
    h_desc = [read.rstrip('\n') for read in open(sys.argv[2])]
    skippableChars = 16

    h_E = h_desc[0][skippableChars:]
    h_E = list(h_E)

    # Generating new transition table
    global Q
    h_trans = OrderedDict()
    for a in range(Q):
        # Test
        abx = a
        h_trans[a] = OrderedDict()
        for b in h_E:
            #Test
            abx = b
            h_trans[a][b] = ''

    # Saving the h strings
    h_str = h_desc[2:]
    h_str = list(h_str)

    # Moving through h strings to match to new table
    for d, a in enumerate(h_E):
        for b in range(Q):
            S = b
            for c in h_str[d]:
                S = dfa[int(S)][c]
            h_trans[b][a] = S

    print("Number of States: ", Q)
    print(DFA_desc[1])
    print("Alphabet: ", end="")
    for a in h_E:
        print(a, end="")
    print()

    for a in h_trans:
        for b in h_trans[a]:
            print(h_trans[a][b], end="")
        print()



def main():
    readDFA()
    simHomo()

main()
