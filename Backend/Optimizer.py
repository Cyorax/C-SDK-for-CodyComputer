from middleend.DACParser import DAC

class Optimizer():
    def __init__(self,gimple):
        self.parser =gimple
        self.remove_unused_funcs()
        self.constant_folding_propagation()
        
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
    
    def constant_folding_propagation(self):
        for func in self.parser.functions:
            changed = True
            while changed:
                before = func["Instructions"].copy()
                self.constant_folding(func)
                self.dce(func)
                #self.constant_propagation(func)
                changed = before != func["Instructions"]

    def constant_folding(self, func):
        for index in range(len(func["Instructions"])):
            inssplit = func["Instructions"][index].split()
            if inssplit[0] in ["eq","neq","gtq","ltq","lt","gt","add","sub","mult","div","bitand","bitor","and","or","xor","mod","<<",">>","ASR","ASL"]:
                if self.is_number(inssplit[2]) and self.is_number(inssplit[3]):
                    a = int(inssplit[2])
                    b = int(inssplit[3])
                    dest = inssplit[1]
                    match inssplit[0]:
                        case "eq":
                            func["Instructions"][index] = f"assign {dest} 0" if a == b else f"assign {dest} 255"
                        case "neq":
                            func["Instructions"][index] = f"assign {dest} 0" if a != b else f"assign {dest} 255"
                        case "gt":
                            func["Instructions"][index] = f"assign {dest} 0" if a > b else f"assign {dest} 255"
                        case "lt":
                            func["Instructions"][index] = f"assign {dest} 0" if a < b else f"assign {dest} 255"
                        case "gtq":
                            func["Instructions"][index] = f"assign {dest} 0" if a >= b else f"assign {dest} 255"
                        case "ltq":
                            func["Instructions"][index] = f"assign {dest} 0" if a <= b else f"assign {dest} 255"
                        case "add":
                            func["Instructions"][index] = f"assign {dest} {a + b}"
                        case "sub":
                            func["Instructions"][index] = f"assign {dest} {a - b}"
                        case "mult":
                            func["Instructions"][index] = f"assign {dest} {a * b}"
                        case "div":
                            func["Instructions"][index] = f"assign {dest} {a // b}"
                        case "mod":
                            func["Instructions"][index] = f"assign {dest} {a % b}"
                        case "bitand":
                            func["Instructions"][index] = f"assign {dest} {a & b}"
                        case "bitor":
                            func["Instructions"][index] = f"assign {dest} {a | b}"
                        case "xor":
                            func["Instructions"][index] = f"assign {dest} {a ^ b}"
                        case "<<":
                            func["Instructions"][index] = f"assign {dest} {a << b}"
                        case ">>":
                            func["Instructions"][index] = f"assign {dest} {a >> b}"
                        case "ASR":
                            func["Instructions"][index] = f"assign {dest} {a >> 1}" 
                        case "ASL":
                            func["Instructions"][index] = f"assign {dest} {a << 1}"
                        case _:
                            pass
            elif(inssplit[0] == "if" and self.is_number(inssplit[1])):
                func["Instructions"][index] = f"goto {inssplit[2]}"  if(int(inssplit[1]) == 0) else f"goto {inssplit[3]}"
        return
    
    
    def constant_propagation(self,func):
        locals = [x for x in func["locals"]]
        blocks,edges = self.constructCFG(func)
        for b in blocks:
            pass
        
        
        
        
        
        
        
    def dce(self,func):
        blocks,edges = self.constructCFG(func)
        used_blocks = self.dce_on_cfg(edges)
        func["Instructions"] = self.unite_blocks(blocks, used_blocks)
        
    def dce_on_cfg(self, edges):
        start = "initnode"
        queue = [start]
        visited = {start}
    
        while queue:
            cur = queue.pop(0)
            for adj in edges.get(cur, []):
                if adj not in visited:
                    visited.add(adj)
                    queue.append(adj)
    
        return visited
    

    def unite_blocks(self,blocks,which):
        res = []
        for block in blocks:
            if block in which:
                res += blocks[block]
        return res
    
    
    def constructCFG(self,func):
        curlabel = "initnode"
        curinstructions = []
        nodes = {}
        edges = {}
        edges[curlabel] = set()
        dead = False
        for i in func["Instructions"]:
            if(i.startswith("label")):
                nodes[curlabel] = curinstructions
                if not dead:
                    edges[curlabel].add(i.split()[1])
                curlabel = i.split()[1]
                edges[curlabel] = set()
                curinstructions = []
                curinstructions.append(i)
                dead = False
            elif(i.startswith("goto")):
                curinstructions.append(i)
                edges[curlabel].add(i.split()[1])
                dead = True
            elif(i.startswith("if") and not dead):
                curinstructions.append(i)
                #if cond label label
                isplit = i.split()
                edges[curlabel].add(isplit[2])
                edges[curlabel].add(isplit[3])
                dead = True
            elif(i.startswith("return") and not dead):
                curinstructions.append(i)
                dead = True
            elif(not dead):
                curinstructions.append(i)
        nodes[curlabel] = curinstructions
        return nodes,edges
    
    def is_number(self,ident):
        return all(ch in "0,1,2,3,4,5,6,7,8,9".split(",") for ch in ident) or ident[0]=="-" and all(ch in "0,1,2,3,4,5,6,7,8,9".split(",") for ch in ident[1:])
    
    def is_local(self,ident,locallist):
        return ident[0]=="_" or ident in locallist
    