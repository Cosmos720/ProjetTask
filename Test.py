from ParTask import *

W = None
X = None
Y = None
Z = None

def runT0():
    global X
    X=X
def runT1():
    global X
    X = 25
def runT2():
    global Y
    Y = 3
def runT3():
    global Y
    Y = Y
def runT4():
    global X
    X = X
def runTsomme():
    global X, Y, Z
    Z = X + Y
def runT5():
    global X, Y, W
    W = X + Y

t0 = Task("T0", ["X"], ["X"], runT0)

t1 = Task("T1", write=["X"], fonction=runT1)

t2 = Task("T2", write=["Y"], fonction=runT2)

t3 = Task("T3", ["Y"], ["Y"], runT3)

t4 = Task("T4", ["X"], ["X"], runT4)

tSomme = Task("somme", ["X", "Y"], ["Z"], runTsomme)

t5 = Task("T5", ["X", "Y"], ["W"], runT5)

s1 = TaskSystem([t1, t2, t3, t4, tSomme, t5])

s1.run()

print(X)
print(Y)
print(Z)
print(W)