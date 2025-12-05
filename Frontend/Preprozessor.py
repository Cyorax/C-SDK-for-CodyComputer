from Frontend import CTokenizer

class Preprozessor:
    
    def __init__(self,tok):
        self.tok = tok
        self.expanded = []
        self.systemslibs = ["Codymath.h"]
        while(tok.next()=="#"):
            self.expand_includes()
        tok.set_pointer(0)# das hier hat mich eine Stunde debuggen gekostet um zu verstehen, dass ich den pointer veränder und das gleiche Objekt in der Main weitergebe
        
    def get_syslibs(self):
        return set(self.systemslibs)
    
    def expand_includes(self):
        self.tok.advance()
        if(self.tok.next() == "include"):
            self.tok.advance()
            if(self.tok.next() == "<"):
                self.tok.advance()
                headerfile = self.tok.consume_cur()
                self.inside_headerfile(f"lib/{headerfile}")
                self.systemslibs.append(headerfile)
                line = self.tok.get_line()
                self.tok.drop_line(line)
                for x in self.expanded:
                    self.tok.append_toline(line,x)
                self.expanded = []
                self.tok.advance()
                return
            elif self.tok.next() == "\"":
                self.tok.advance()
                headderfile = self.tok.consume_cur()
                self.inside_headerfile(headderfile)
                line = self.tok.get_line()
                self.tok.drop_line(line)
                for x in self.expanded:
                    self.tok.append_toline(line,x)
                self.expanded = []
                self.tok.advance()
                return
        #self.tok.drop_line(self.tok.get_line())
            
    def inside_headerfile(self,path):
        tok = CTokenizer.Tokenizer(path)
        self.read_headerfile(tok)
        
    def read_headerfile(self, tok):
        while tok.next() != "EOF":
            if tok.next() == "#":
                tok.advance()
                operation = tok.next()
                if operation == "include":
                    tok.advance()
                    if tok.next() == "<":
                        tok.advance()
                        headerfile = tok.consume_cur()
                        self.systemslibs.append(headerfile)
                        self.inside_headerfile(f"lib/{headerfile}")
                        tok.eat(">")
                    elif tok.next() == "\"":
                        tok.advance()
                        headerfile = tok.consume_cur()
                        self.inside_headerfile(headerfile)
                        tok.eat("\"")
                elif operation == "define":
                    return
            else:
                while tok.next() not in ["EOF", ";"]:
                    self.expanded.append(tok.consume_cur())
                if tok.next() == ";":
                    self.expanded.append(tok.consume_cur())


        