from threading import Thread
import pygraphviz as pgv



class Task:
    """Crée une tâche à utiliser dans un système de tâche"""
    name = str()
    reads = list()
    writes = list()
    run = None

    def __init__(self, name = "", read = [], write = [], fonction = None):
        self.name=name
        self.reads=read
        self.writes=write
        self.run=fonction
        self.verifError()

    def verifError(self):
        """Vérifie les erreurs de création d'une tâche"""
        Erreur = False
        if self.name == "":
            print("Erreur: Création d'une tâche sans nom!!!")
            exit()
        if not(hasattr(self.run,'__call__')):
            print("Une tâche doit posseder une fonction à effectuer!!!")
            Erreur = True
        if self.reads == [] and self.writes == []:
            print("Une tache ne peut pas avoir son domaine de lecture ET d'écriture vide !!!")
            Erreur = True
        
        if(Erreur):
            print(("Erreur sur la tache {}").format(self))
            exit()

    def __repr__(self):
        return self.name

class TaskSystem:
    """Crée un systeme de tâche de parallelisme maximale"""
    taskList = list()
    ordre = dict()
    dependance = dict()
    effectuer = list()
    threads = list()

    def __init__(self, taskList = []):
        """Ecrire la liste des tâche dans l'ordre d'execution voulu"""
        self.taskList = taskList
        self.verrifError()
        self.ordre = {task:[] for task in self.taskList}
        self.calcDico()
        self.calcDepedencies()
        self.dessin()

    def verrifError(self):
        """Vérifie les erreurs de création d'un systeme de tâche"""
        Erreur = False
        if self.taskList == []:
            print("Erreur le systeme de tâche ne possede aucune tâche à effectuer!!!")
            Erreur = True
        for i in range(len(self.taskList)):
            for j in range(i+1,len(self.taskList)):
                if self.taskList[i].name == self.taskList[j].name:
                    print(("Erreur le nom de tâche {} apparait deux fois dans le systeme de tâche!!!").format(self.taskList[i].name))
                    Erreur = True
                    break
                    
        if Erreur:
            exit()


    def calcDico(self):
        """Crée le dictionnaire des dépendances pour un systeme de tâche en ligne"""
        for i in range(len(self.taskList)):
            for j in range(i,-1,-1):
                self.ordre[self.taskList[i]] += [self.taskList[j]]


    def calcDepedencies(self):
        """Calcul de la minimisation maximale du systeme de tâche"""
        for t1 in self.taskList:
            dep=[]
            for t2 in self.ordre[t1]:
                if t1 != t2 and not(self.Bernstein(t1, t2)):
                    dep.append(t2)
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



    def dessin(self):
        """Dessine le systeme de tâche sous la forme d'un graphe"""
        graph = pgv.AGraph(directed=True)
        for key in self.dependance.keys():
            if not (self.dependance[key]==[]):
                for value in self.dependance[key]:
                    graph.add_edge(value.name, key.name)
        graph.layout('dot')
        graph.draw('Graphe.png')
        graph.close()
                
    
    def Bernstein(self, t1, t2):
        """Calcul les conditions de bernstein entre les tâches t1 et t2"""
        if((set(t1.reads) & set(t2.writes))==set()):
            if((set(t1.writes) & set(t2.reads))==set()):
                if((set(t1.writes) & set(t2.writes))==set()):
                    return True
        return False
    
    def getDepedencies(self, task):
        """Renvoie les tâches desquelles dependent task"""
        dep = []
        for key, value in self.dependance.items():
            if task==key:
                for v in value:
                    dep.append(v)
                return dep
        
    def execution(self, task):
        """Execution de la tâche task apres l'execution des tâches dont elle dépend"""
        taskWait = []
        for t in self.getDepedencies(task):
            taskWait.append(t.name)
            if not(self.effectuer.__contains__(t)):
                self.effectuer.append(t)
                thread = Thread(name=t.name, target=self.execution, args=[t])
                thread.start()
                self.threads.append(thread)
        
        for t in self.threads:
            if taskWait.__contains__(t.getName()):
                t.join()
        
        task.run()
        print(task.name + " à fini de s'executer")

    def calculLastTask(self):
        """Renvoie la liste des tâches qui doivent s'effectuer en dernier"""
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
        return tasks

    def run(self):
        for task in self.calculLastTask():
            self.effectuer += task.name
            self.execution(task)