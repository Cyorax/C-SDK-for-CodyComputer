class Tokenizer:

    def __init__(self, tokenstring):
        self.tokenlist = self.tokenize(tokenstring)
        self.cur = 0
        self.curmethod = ""
        
    def get_pointer(self):
        return self.cur
    
    def set_pointer(self,value):
        self.cur = value
    
    def advance(self):
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
        if self.next() == token:
            self.advance()
            return 
        raise Exception(f"Expected {token} got {self.next()} in function {self.curmethod}")
    
    def next(self, nex = 0): 
        return "EOF" if self.cur+nex >= len(self.tokenlist) else self.tokenlist[self.cur+nex]
       
    def tokenize(self, tokenstring: str):
        SYMBOLS = ["+", "-", "*", "/", "=", ";", "{", "}", "(", ")", ",","<",">"]
        s = tokenstring.replace("\n", " ").replace("\t", " ")
        for sym in SYMBOLS:
            s = s.replace(sym, f" {sym} ")
        tokens = s.split()
        return tokens
