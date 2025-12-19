class Tokenizer:

    def __init__(self, filepath, fromfile = True):
        if(fromfile):
            self.file = filepath.split("/")[-1]
            f = open(filepath, "r")
            lines = "" 
            lc = 1;
            inmulti = False
            for  line in f:
                if("/*" in line and not inmulti):
                    inmulti = True
                    lines += "."+str(lc)+" "+line.split("/*")[0].split("//")[0].lstrip()
                    lc += 1
                    
                if("*/" in line and inmulti):
                    inmulti = False
                    lines += "."+str(lc)+" "+line.split("*/")[1].split("//")[0].rstrip()
                    lc += 1
                    continue
                
                if(inmulti):
                    continue
                else:
                    lines += "."+str(lc)+" "+line.split("//")[0]
                    lc += 1
        else:
            lines = filepath
            self.file = "test"
        self.tokenlist = self.tokenize(lines)
        self.cur = 0
        self.linecounter = 0
        self.curmethod = ""
        self.doubles = ["==", "!=", "<=", ">=", "<<", ">>", "&&", "||","++","--","+=","-=","*=","/=","%=","&=","^=","|="]
        
    def get_pointer(self):
        return self.cur
    
    def set_pointer(self,value):
        self.cur = value
        
    def drop_line(self,line):
        index = self.tokenlist.index("."+str(line)) + 1
        while(not self.tokenlist[index].startswith(".")):
            self.tokenlist.pop(index)
    
    def append_toline(self,line,code):
        index = self.tokenlist.index("."+str(line+1))
        self.tokenlist.insert(index,code)
        
    def set_pointer_next_line(self,line):
        index = self.tokenlist.index("."+str(line+1))
        self.set_pointer(index)
    
    def advance(self):
        while(self.cur < len(self.tokenlist) and self.tokenlist[self.cur][0]=="."):
            self.linecounter = int(self.tokenlist[self.cur][1:])
            self.cur += 1
        self.cur += 1
        
    def get_line(self):
        return self.linecounter
        
    def consume_cur(self):
        n = self.next()
        self.advance()
        if(n in self.doubles):
            self.advance()
        return n
    
    def get_next_tok_num(self):
        return self.cur
    
    def get_tokens(self):
        return self.tokenlist
    
    def get_remaining(self):
        return self.tokenlist[self.cur:]
    
    def eat(self,token):
        a = self.next()
        if a == token:
            self.advance()
            return 
        print(f"Expected {token} got {a} in line {self.linecounter} in file {self.file}")
        
    def next(self,nex = 0):
        if(str(self.nex(nex) + self.nex(nex+1)) in self.doubles):
            return str(self.nex(nex) + self.nex(nex+1))
        else:
            return str(self.nex(nex))
    def print_tokens(self):
        i = 0
        while(i < len(self.tokenlist)):
                i += 1
                print(self.next(i))
        
    def nex(self, nex):
        i = self.cur
        while i < len(self.tokenlist) and self.tokenlist[i].startswith("."):
            self.linecounter = int(self.tokenlist[i][1:])
            i += 1
        s = nex
        while s > 0 and i < len(self.tokenlist):
            i += 1
            while i < len(self.tokenlist) and self.tokenlist[i].startswith("."):
                self.linecounter = int(self.tokenlist[i][1:])
                i += 1
            s -= 1
        if i >= len(self.tokenlist):
            return "EOF"
        return self.tokenlist[i]
        
    def tokenize(self, tokenstring: str):
        SYMBOLS = ["#","+", "-", "*", "/", "=", ";", "{", "}", "(", ")", ",","<",">","!","|","&","?",":","[","]"]
        s = tokenstring.replace("\n", " ").replace("\t", " ")
        for sym in SYMBOLS:
            s = s.replace(sym, f" {sym} ")
        tokens = s.split()
        return tokens
    
    def is_ident(self,ident):
        return ident.lower()[0] in "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")
    
    def is_number(self,ident):
        return all(ch in "0,1,2,3,4,5,6,7,8,9".split(",") for ch in ident)
    
    def is_character(self,ident):
        return ident[0] == "'" and ident[-1] == "'"
        
