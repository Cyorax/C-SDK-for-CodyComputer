#temp variablen beginnen mit _

##DatenTypen:
# int 16 Bit -32768 bis 32767
# char 8 Bit 0 bis 255
# short 8 Bit -128 bis 127
# pointer 16 Bit 64k

class Gimple():
    
    def __init__(self, tokenizer):
        self.tok = tokenizer
        self.datatypes = {"int":2,"char":1,"pointer":2}
        self.parse_globals()
        self.parse_functions()
        
    def dump_gimple(self):
        print(self.globalsmap)
        print(self.functions)
        
    def merge(self,gimp):
        for i in gimp.globalsmap.keys():
            self.globalsmap[i]=gimp.globalsmap[i]
        for f in gimp.functions:
            self.functions.append(f)
        
    def get_Globals(self):
        return self.globalsmap
    def get_Functions(self):
        return self.functions
        
    def parse_globals(self):
        self.globalcount = 0
        self.globalsmap = {} 
        while(self.parse_globalline()):
            pass
    
    def parse_globalline(self):
        if self.tok.next(2) == "=" or self.tok.next(2) == ";":
            typ = self.tok.consume_cur()
            ident = self.tok.consume_cur()
            if(self.tok.next() == "="):
                self.tok.eat("=")# skip =
                initvalue = self.tok.consume_cur()
                self.tok.eat(";") # skip ;
            else:
                self.tok.eat(";") # skip ;
                initvalue = "null"
            self.globalsmap[ident] = {"offset":self.globalcount,"type":typ,"value":initvalue}
            self.globalcount += self.datatypes.get(typ)
            return True
        return False
    
    def parse_functions(self):
        self.functions = []
        while(self.parse_function()):
            if(self.instructions ==[] or "return" not in self.instructions[-1]):
                self.instructions.append("return")
            self.functions.append({"Name":self.funcname,"calledfuncs":self.calledfuncs,"lclmaxoffset":self.lcloffsetcount,"rettype":self.rettype,"locals":self.localtab,"Instructions":self.instructions})
            
    def parse_function(self):
        self.localtab = {}
        self.funcname = None
        self.rettype = None
        self.argoffsetcount = 0
        self.lcloffsetcount = 0
        self.calledfuncs = []
        if(self.parse_functionheadder()):
            self.parse_locals()
            self.instructions=[]
            self.parse_instructions()
            self.tok.eat("}")
            return True
        return False
    
    def addInstruktion(self,inst):
        self.instructions.append(inst)
    
    def parse_functionheadder(self):
        n = self.tok.next()
        if n != "EOF":
            rettype, funcname = self.parse_type()
            
            self.rettype = rettype
            self.funcname = funcname
            
            self.tok.eat("(")
            if self.tok.next() == "void":
                self.tok.advance()
            else:
                while self.tok.next() != ")":
                    argtype,argident = self.parse_type()
                    self.localtab[argident] = {
                        "type": argtype,
                        "offset": self.argoffsetcount,
                        "location": "arg"
                    }
                    self.argoffsetcount += 2
        
                    if self.tok.next() == ",":
                        self.tok.eat(",")  # skip ,
        
            self.tok.eat(")")   # skip )
            self.tok.eat("{")   # skip {
    
            return True
        return False

    
    def parse_locals(self):
        while(self.parse_local()):
            pass
        
    def parse_local(self):
        if self.tok.next() in self.datatypes:
            typ, ident = self.parse_type()
            self.tok.eat(";")
            self.localtab[ident] = {"type":typ,"size":self.datatypes[typ],"offset":self.lcloffsetcount,"location": "lcl"}
            self.lcloffsetcount += self.datatypes[typ]
            return True
        return False
    
    def parse_instructions(self):
        while(self.parse_instruction()):
            pass
        
    def parse_instruction(self):
        if self.tok.next() == "}":
            return False
        
        if self.tok.next() == "if":
            self.tok.eat("if") # skip if
            op,op1,op2 = self.parse_condition()
            self.tok.eat("goto") # skip goto
            label = self.parse_label()
            self.tok.eat(";")
            if self.tok.next() == "else":  
                self.tok.eat("else") # skip else
                self.tok.eat("goto") # skip goto
                label += " "+self.parse_label()
                self.tok.eat(";") # skip ;
            #Schummeln für vergleiche
            if("gt" not in op):
                self.addInstruktion("if"+" "+op+" "+op1+" "+op2+" "+label) 
            else:
                self.addInstruktion("if"+" "+op+" "+op2+" "+op1+" "+label) 
            return True
        
        elif self.tok.next() == "goto":  
            self.tok.eat("goto") # skip goto
            label = self.parse_label()   
            self.tok.eat(";") 
            self.addInstruktion("goto"+" "+label)
            return True
        
        elif self.tok.next() == "<": 
            label = self.parse_label()
            self.tok.eat(":")
            self.addInstruktion("label"+" "+label)
            return True
        
        elif self.tok.next(1) == "=" or self.tok.next(2) == "=":
            self.parse_statement()
            return True
  
        elif self.tok.next() == "return":
            self.tok.eat("return") # skip return
            value = ""
            if(self.tok.next()!=";"):
                value = " "+self.tok.consume_cur() 
            self.tok.eat(";") # skip ;        
            self.addInstruktion("return"+value)  
            return True 
        
        elif self.tok.next(1) == "(": 
            ident, args = self.parse_funccall()
            self.addInstruktion("call "+ident+" "+args)
            self.tok.eat(";") # skip ;  
            return True
        
        print("PARSING ERROR AT",self.tok.next())

    def parse_type(self):
        type = self.tok.consume_cur()
        if(self.tok.next()=="*"):
            self.tok.advance()
            type = "pointer"
        ident =self.tok.consume_cur()
        return type, ident 
    
    def parse_statement(self):
        dest = self.parse_operand()
        self.tok.eat("=") #skip =
        #Semikolon klammerauf oder Operator   
        match (self.tok.next(1)):
            case "(":
                ident, args = self.parse_funccall()
                self.addInstruktion("call "+ident+" "+args)
                self.addInstruktion("assignret "+dest)
                self.tok.eat(";") #skip ; 
            case _:
                op1 = self.parse_operand()
                if(self.tok.next() != ";"):
                    op = self.parse_opertation()
                    op2 = self.parse_operand() #das hier kann noch eine Funktion sein
                    self.tok.eat(";") #skip ;
                    self.addInstruktion(op+" "+dest+" "+op1+" "+op2)
                else:
                    self.addInstruktion("assign"+" "+dest+" "+op1)
                    self.tok.eat(";") #skip ;    
            

    def parse_operand(self):
        #casted long int short int 
        if(self.tok.next() == "("):
            self.tok.eat("(")
            while(self.tok.next()!=")"):
                self.tok.consume_cur()
            self.tok.eat(")")
        op = ""
        negated = False
        if self.tok.next() == "-":
            self.tok.eat("-")
            op += "neg("
            negated = True
            
        op += self.tok.consume_cur()
        if(op == "*" or op == "&"):
            op += self.tok.consume_cur()
        if(negated):
            op += ")"
        return op
    
    def parse_label(self):
        self.tok.eat("<") # skip <  
        label = self.tok.consume_cur()
        while(self.tok.next()!=">"):
            label += self.tok.consume_cur()
        self.tok.eat(">") # skip > 
        return label.replace(".","") #D. ist nicht gültig als label
    
    def parse_funccall(self):
        ident = self.tok.consume_cur()
        self.tok.eat("(")
        args = ""
        while(self.tok.next()!=")"):
            args += " "+self.tok.consume_cur()
            if(self.tok.next()==","):
                self.tok.advance()
        self.tok.eat(")")
        self.calledfuncs += [ident]
        return ident, args
        
    #mit klammern
    def parse_condition(self):
        self.tok.eat("(")
        op1 = self.parse_operand()
        operation = self.parse_opertation()
        op2 = self.parse_operand()
        self.tok.eat(")")
        return operation,op1,op2
        
    def parse_opertation(self):
        op = self.tok.consume_cur()
        if(self.tok.next()== "="):
            op += self.tok.consume_cur()
        match op:
            case "==":
                return "eq"   
            case "!=":
                return "neq"
            case ">=":
                return "gtq"
            case "<=":
                return "ltq"
            case "<":
                return "lt"
            case ">":
                return "gt"
            case "+":
                return "add"
            case "-":
                return "sub"
            case "*":
                return "mult"
            case "/":
                return "div"
            case "&":
                return "bitand"
            case "|":
                return "bitor"
            case "^":
                return "xor"
            case _:
                print("COULD NOT MATCH OPERATION",op)

