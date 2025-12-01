from middleend.GimpleParser import Gimple

class Optimizer():
    def __init__(self,gimple):
        self.parser =gimple
        self.remove_unused_funcs()
        
    #BFS um die ungenutzen Methoden zu finden und zu entfernen
    def remove_unused_funcs(self):
        self.availablefuncs = ["main"]
        self.queue = ["main"]
        while self.queue != []:
            cur = self.queue.pop(0)
            for i in self.get_successors(cur):
                if i not in self.availablefuncs:
                    self.availablefuncs.append(i)
                    self.queue.append(i)
        self.parser.functions = [f for f in self.parser.functions if f["Name"] in self.availablefuncs]

        
    def get_successors(self,func):
        f = self.get_Func(func)
        if len(f) == 0:
            raise Exception("Called function with name: "+func+" not found")
        return f[0]["calledfuncs"]
    
    def get_Func(self,name):
        return [s for s in self.parser.functions if s["Name"]==name]
    