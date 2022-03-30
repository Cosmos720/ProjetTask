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

t0 = Task("T0", runT0, r=["X"])

t1 = Task("T1", runT1, w=["X"])

t2 = Task("T2", runT2, w=["Y"])

t3 = Task("T3", runT3, ["Y"], ["Y"])

t4 = Task("T4", runT4, ["X"], ["X"])

tSomme = Task("somme", runTsomme, ["X", "Y"], ["Z"])

t5 = Task("T5", runT5, ["X", "Y"], ["W"])

s1 = TaskSystem([t1, t2, t3, t4, tSomme, t5])

s1.run()

print(X)
print(Y)
print(Z)
print(W)