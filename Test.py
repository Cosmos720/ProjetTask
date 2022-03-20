from ParTask import *

X = None
Y = None
Z = None

def runT1():
    global X
    X = 1

def runT2():
    global Y
    Y = 2

def runTsomme():
    
    global X, Y, Z
    Z = X + Y

t1 = Task("T1", [], ["X"], runT1)

t2 = Task("T2", [], ["Y"], runT2)

tSomme = Task("somme", ["X","Y"], ["Z"], runTsomme)

s1 = TaskSystem([t1, t2, tSomme], {"T1": [], "T2": [t1], "somme": [t1, t2]})

print(s1.getDepedencies("somme"))

s1.run()

print(Z)