from ast import Global
from concurrent.futures import thread
from threading import Thread, Semaphore
import pygraphviz as pg



class Task:
    name = ""
    reads = []
    writes = []
    run = None

    def __init__(self, n, f, r = [], w = []):
        self.name=n
        self.reads=r
        self.writes=w
        self.run=f

    def __repr__(self):
        return self.name

class TaskSystem:
    taskList = []
    ordre = {}
    dependance = {}
    effectuer = []
    sem = Semaphore(0)
    threads = []

    def __init__(self, taskList):
        self.taskList = taskList
        self.ordre = {task:[] for task in self.taskList}
        self.calcDico()
        self.calcDepedencies()
        self.sem = Semaphore(len(self.taskList))

    def calcDico(self):
        for task in range(len(self.taskList)):
            for dep in range(task,-1,-1):
                self.ordre[self.taskList[task]] += [self.taskList[dep]]


    def calcDepedencies(self):
        for t1 in self.taskList:
            dep=[]
            for t2 in self.ordre[t1]:
                if t1 != t2 and not(self.Bernstein(t1, t2)):
                    dep += [t2]
            self.dependance[t1] = dep
        for key in self.dependance.keys():
            redond = []
            for value in self.dependance[key]:
                if self.dependance[value] != []:
                    inter = list(set(self.dependance[key]) & set(self.dependance[value]))
                    for x in inter:
                        if not(redond.__contains__(x)):
                            redond.append(x)
            for x in redond:
                self.dependance[key].remove(x)



    def test(self):
        graph = pg.AGraph(directed=True)
        for key in self.dependance.keys():
            if not (self.dependance[key]==[]):
                for value in self.dependance[key]:
                    graph.add_edge(value.name, key.name)
        graph.layout('dot')
        graph.draw('Graphe.png')
        graph.close()
                
    
    def Bernstein(self, t1, t2):
        if((set(t1.reads) & set(t2.writes))==set()):
            if((set(t1.writes) & set(t2.reads))==set()):
                if((set(t1.writes) & set(t2.writes))==set()):
                    return True
        return False
    
    def getDepedencies(self, nomTask):
        dep = []
        for key, value in self.dependance.items():
            if nomTask==key:
                for v in value:
                    dep.append(v)
                return dep
        
    def speedrun(self, task):
        taskWait = []
        for t in self.getDepedencies(task):
            taskWait.append(t.name)
            if not(self.effectuer.__contains__(t)):
                self.effectuer.append(t)
                thread = Thread(name=t.name, target=self.speedrun, args=[t])
                thread.start()
                self.threads.append(thread)
        
        for t in self.threads:
            if taskWait.__contains__(t.getName()):
                t.join()
        
        task.run()
        print(task.name + " à fini de s'executer")

    def run(self):
        self.test()
        tasks = []
        for task in self.dependance.keys():
            last = True
            for t in self.dependance.keys():
                if task != t:
                    if self.dependance[t].__contains__(task):
                        last = False
                        break
            if last:
                tasks.append(task)
        self.effectuer += tasks

        taskWait = []
        for task in tasks:
            taskWait.append(task.name)
            thread = Thread(name=task.name, target=self.speedrun, args=[task])
            thread.start()
            self.threads.append(thread)

        for t in self.threads:
            if taskWait.__contains__(t.getName()):
                t.join()
        
