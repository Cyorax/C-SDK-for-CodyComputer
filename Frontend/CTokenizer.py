class Tokenizer:

    def __init__(self, tokenstring):
        self.tokenlist = self.tokenize(tokenstring)
        self.cur = 0
        self.linecounter = 0
        self.eof_counter = 0;
        self.curmethod = ""
        
    def get_pointer(self):
        return self.cur
    
    def set_pointer(self,value):
        self.cur = value
    
    def advance(self):
        while(self.cur < len(self.tokenlist) and self.tokenlist[self.cur][0]=="."):
            self.linecounter = int(self.tokenlist[self.cur][1:])
            self.cur += 1
        self.cur += 1
        
    def consume_cur(self):
        n = self.next()
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
        print(f"Expected {token} got {a} in line {self.linecounter}")
    
    def next(self, nex=0):
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
        SYMBOLS = ["#","+", "-", "*", "/", "=", ";", "{", "}", "(", ")", ",","<",">"]
        s = tokenstring.replace("\n", " ").replace("\t", " ")
        for sym in SYMBOLS:
            s = s.replace(sym, f" {sym} ")
        tokens = s.split()
        return tokens
