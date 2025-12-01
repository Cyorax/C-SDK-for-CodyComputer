from Frontend.CTokenizer import Tokenizer
#todo temp variablen Reusen nach einer Instruktion durchdenken müsste aber eigentlich
#todo operatoren parsen, 

class CParser:

    def __init__(self, tok):
        self.tok = tok
        self.final_code = []
        self.globals = []
        self.controllstrukturencounter = 0;
        self.types = ["char","int","short","void"]
        self.parse()

    def create_label(self):
        self.controllstrukturencounter += 1
        return "<c."+self.controllstrukturencounter+">"
    
    def generate_gimple(self):
        return str(self.globals+self.final_code)
        
        
    def parse(self):
        if(self.tok.next() == "EOF"):
            self.generate_gimple()
            return 
        back = self.tok.get_pointer()
        pg = self.parse_global()
        if(not pg):
            self.tok.set_pointer(back)
            self.locals = []
            self.instructions = []
            self.temp = 0
            functionhead = self.parse_function()
            self.final_code += [functionhead] + self.locals + self.instructions + ["}"]
        self.parse()
        
    def parse_function(self):
        type, ident = self.parse_type()
        self.tok.curfunc = ident
        self.tok.eat("(")
        args = ""
        if(self.tok.next() == "void"):
            self.tok.advance()
        while(self.tok.next()!=")"):
            argtype, argident = self.parse_type()
            args += argtype+" "+argident
            if(self.tok.next() == ","):
                self.tok.advance()
                args += ","
        self.tok.advance()
        self.tok.eat("{")
        self.parse_functionbody()
        self.tok.eat("}")
        return f"{type} {ident}({args})"+"{"
        #self.finalcode.append(locals) und dann instructions
        
    #bei deklaration nichts speichern nur locals appenden bei init appenden und ident = value zu instructions appenden
    def parse_functionbody(self):
        while(self.tok.next() != "}"):
            self.parse_instructions()
            
    def parse_instructions(self):
        while(self.tok.next() != "}"):
            self.parse_instruction()
    
        
    def parse_instruction(self):
        match(self.tok.next()):
            case "{":
                self.tok.eat("{")
                self.parse_instructions()
                self.tok.eat("}")
                
            case "if":
                self.tok.eat("if")
                self.tok.eat("(")
                self.parse_expression()
                self.tok.eat(")")
                if(self.tok.next() == "{"):
                    self.tok.eat("{")
                    self.parse_instructions()
                    self.tok.eat("}")
                    #hier else
                else:
                    self.parse_instruction()
                    #hier else
                
                return
                
            case "while":
                self.tok.eat("while")
                self.tok.eat("(")
                self.parse_expression()
                self.tok.eat(")")
                if(self.tok.next() == "{"):
                    self.tok.eat("{")
                    self.parse_instructions()
                else:
                    self.parse_instruction()
                
                return 
            
            case "return":
                self.tok.eat("return")
                self.parse_expression()
                self.tok.eat(";")
                
            case _:#init, dec, assign oder functioncall
                if self.tok.next() in self.types:
                    type,ident = self.parse_type()
                    if(self.tok.next()=="="):
                        self.tok.eat("=")
                        self.parse_expression()
                        self.tok.eat(";")
                    elif(self.tok.next()==";"):
                        self.tok.eat(";")
                    self.locals.append(f"{type} {ident};")
                    
                elif self.tok.next(1) == "(":
                    self.parse_functioncall()
                    self.tok.eat(";")
                    
                elif self.tok.next()!="}":
                    op = self.parse_operand()
                    self.tok.eat("=")
                    self.parse_expression()
                    self.tok.eat(";")
                return
            
    def parse_operand(self):
        #casted long int short int 
        if(self.tok.next() == "("):
            self.tok.eat("(")
            while(self.tok.next()!=")"):
                self.tok.consume_cur()
            self.tok.eat(")")
        op = self.tok.consume_cur()
        while(op == "*"):
            op += self.parse_ident()
        #hier noch Array hinzufügen theoretisch kann man einfach die Addresse nehemen und dann draufaddieren 
        return op
  
    #follow ist ; und ) , 
    def parse_expression(self):
        while(self.tok.next()!=";" and self.tok.next()!=")" and self.tok.next()!=","):
            self.parse_expres()
            
            
    #operatoren liste :
    # &&,&,||,|,<=,>=,<,>,==,!=,^,+,-,/,*,%,++,--,? :,+=,-=,*=,/=,>>,<<
    #unär: 
    # - ! 
    #addition subtraktion mult div shift comperators 
    def parse_expres(self):
        #hier alles versuchen zu parsen mit loop auf parse expres
        
        
        
        if(self.tok.next()=="("):
            self.tok.eat("(")
            self.parse_expression()
            self.tok.eat(")")
            return
        
        if(self.tok.next(1)=="("):
            self.parse_functioncall()
            return
        
        if(self.tok.next()=="*"):
            self.tok.eat("*")
            self.parse_expression()
            return 
        
        if(self.tok.next()=="-"):
            self.tok.eat("-")
            self.parse_expression()
            return 
        
            # hier int und ident und dann hier am besten auch den check, ob ident schon defininiert ist oder überhauput definiert ist 
        
        return
        
    
    def parse_functioncall(self):
        ident = self.parse_ident()
        self.tok.eat("(")
        while(self.tok.next()!=")"):
            self.parse_expression()
            if(self.tok.next == ","):
                self.tok.advance()
        self.tok.eat(")")
        return 
            
    def parse_condition(self):
        
        return
    #wir müssen not im Baum runterbringen und dann 
    def rewrite_condition(self,condition):
        
        return
    
    
    def parse_global(self):
        type,ident = self.parse_type()
        if(self.tok.next()=="="):
            self.tok.advance()
            int = self.parse_int()
            self.tok.eat(";")
            self.globals.append(f"{type} {ident} = {int};")
            return True
        elif(self.tok.next()==";"):
            self.tok.advance()
            self.globals.append(f"{type} {ident};")
            return True
        else:
            return False
        
    def parse_type(self):
        type = self.tok.consume_cur()
        while(self.tok.next()=="*"):
            self.tok.advance()
        ident = self.tok.consume_cur()
        return type, ident 
    

    
    def parse_ident(self):
        ident = self.tok.consume_cur()
        abc = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(",")
        if(ident.lower()[0] not in abc):
            print("VARIABLE NAME ERROR "+ident+" not possible as variablename")
        return ident
    
    def parse_int(self):
        ident = self.tok.consume_cur()
        nums = "0,1,2,3,4,5,6,7,8,9".split(",")
        s = ident
        if s.startswith("-"):
            s = s[1:]
        if not all(ch in nums for ch in s):
            print("COULD NOT PARSE INT OF VALUE " + ident)
        return ident

        
        
        
        
        