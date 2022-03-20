from threading import Thread

class Task:
    name = ""
    reads = []
    writes = []
    run = None

    def __init__(self, n, r, w, f):
        self.name=n
        self.reads=r
        self.writes=w
        self.run=f

class TaskSystem:
    taskList = []
    dico = {}
    dependance = {}

    def __init__(self, taskList,dico):
        self.taskList = taskList
        self.dico = dico
        self.calcDepedencies()

    def calcDepedencies(self):
        for t1 in self.taskList:
            dep=[]
            for t2 in self.dico[t1.name]:
                if t1 != t2 and not(self.Bernstein(t1, t2)):
                    dep += [t2.name]
            self.dependance[t1.name] = dep
                
    
    def Bernstein(self, t1, t2):
        if((set(t1.reads) & set(t2.writes))==set()):
            if((set(t1.writes) & set(t2.reads))==set()):
                if((set(t1.writes) & set(t2.writes))==set()):
                    return True
        return False
    
    def getDepedencies(self, nomTask):
        print(self.dependance)

    def run(self):
        for t in self.taskList:
            t.run()
            
