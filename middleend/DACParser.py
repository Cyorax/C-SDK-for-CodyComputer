#temp variablen beginnen mit _

##DatenTypen:
# int 16 Bit -32768 bis 32767
# short 8 Bit 0 bis 255
# pointer 16 Bit 64k
# "boolean" 1 und 0

class DAC():
    
    def __init__(self, tokenizer):
        self.tok = tokenizer
        self.datatypes = {"int":2,"short":1,"char":1,"pointer":2,"pointer onebyte":2}
        self.parse_globals()
        self.parse_functions()
        
    def dump_gimple(self):
        print(self.globalsmap)
        for f in self.functions:
            print("\n",f)
        
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
    # da wir durch pointer usw. keinen festen Lookahead haben backtracke ich einfach  
    # mit Backtracking wir gehen zuerst davon aus, dass das was Kommt eine Globale var ist und keine FUnktion 
    def parse_globalline(self):
        ret = self.tok.get_pointer()
        typ,ident = self.parse_type()
        if(self.tok.next()=="("):
            self.tok.set_pointer(ret)
            return False
        if(self.tok.next() == "="):
            self.tok.eat("=")# skip =
            initvalue = self.parse_operand()
            self.tok.eat(";") # skip ;
        else:
            self.tok.eat(";") # skip ;
            initvalue = "null"
        self.globalsmap[ident] = {"offset":self.globalcount,"type":typ,"value":initvalue}
        self.globalcount += 2
        return True
        
    def parse_functions(self):
        self.functions = []
        while(self.parse_function()):
            if(self.instructions ==[] or "return" not in self.instructions[-1]):
                self.instructions.append("return")
            self.functions.append({"Name":self.funcname,"calledfuncs":self.calledfuncs,"lclmaxoffset":self.lcloffsetcount,"locals":self.localtab,"Instructions":self.instructions})
            
    def parse_function(self):
        self.localtab = {}
        self.funcname = None
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
            _, funcname = self.parse_type()
            
            self.funcname = funcname
            self.tok.curmethod = funcname
            
            self.tok.eat("(")
            if self.tok.next() == "void":
                self.tok.advance()
            else:
                while self.tok.next() != ")":
                    argtype,argident = self.parse_type()
                    self.localtab[argident] = {
                        "type": argtype,
                        "size":self.datatypes[argtype],
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
            self.lcloffsetcount += self.datatypes[typ]
            self.localtab[ident] = {"type":typ,"size":self.datatypes[typ],"offset":self.lcloffsetcount,"location": "lcl"}
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
            op = self.parse_operand()
            self.tok.eat("goto") # skip goto
            label = self.parse_label()
            self.tok.eat(";")
            if self.tok.next() == "else":  
                self.tok.eat("else") # skip else
                self.tok.eat("goto") # skip goto
                label += " "+self.parse_label()
                self.tok.eat(";") # skip ;
            self.addInstruktion("if "+ op +" "+label) 
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
  
        elif self.tok.next() == "return":
            self.tok.eat("return") # skip return
            value = ""
            while(self.tok.next()!=";"):
                value += self.tok.consume_cur() 
            self.tok.eat(";") # skip ;        
            self.addInstruktion("return "+value)  
            return True 
        
        elif self.tok.next(1) == "(": 
            ident, args = self.parse_funccall()
            self.addInstruktion("call "+ident+args)
            self.tok.eat(";") # skip ;  
            return True
        
        else:
            self.parse_statement()
            return True

    def parse_type(self):
        type = self.tok.consume_cur()
        if(self.tok.next()=="*"):
            while(self.tok.next()=="*"):
                self.tok.advance()
            type = "pointer" if self.datatypes[type] == 2 else "pointer onebyte"
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
                    if("gt" in op):
                        self.addInstruktion(op+" "+dest+" "+op2+" "+op1)
                    else:
                        self.addInstruktion(op+" "+dest+" "+op1+" "+op2)
                else:
                    self.addInstruktion("assign"+" "+dest+" "+op1)
                    self.tok.eat(";") #skip ;    
            
    
    def parse_operand(self):
        if(self.tok.next() in ["*","&","-"]):
            tok = self.tok.consume_cur()
            val = self.parse_operand()
            return f"{tok}{val}"
        else:
            return self.tok.consume_cur()
            
    
    def parse_label(self):
        self.tok.eat("<") # skip <  
        label = self.tok.consume_cur()
        while(self.tok.next()!=">"):
            label += self.tok.consume_cur()
        self.tok.eat(">") # skip > 
        label = label.replace(".","")
        return label #D. ist nicht gültig als label
    
    def parse_funccall(self):
        ident = self.tok.consume_cur()
        self.tok.eat("(")
        args = ""
        while(self.tok.next()!=")"):
            value = ""
            while(self.tok.next()!="," and self.tok.next()!=")" ):
                value += self.tok.consume_cur()
            if(self.tok.next() == ","):
                self.tok.eat(",")
            args += " "+value;
        self.tok.eat(")")
        self.calledfuncs += [ident]
        return ident, args
        
        
    def parse_opertation(self):
        op = self.tok.consume_cur()
        if(self.tok.next() in ["=","|","&","<",">"]):
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
                self.calledfuncs += ["mult"]
                return "mult"
            case "/":
                self.calledfuncs += ["div"]
                return "div"
            case "&":
                return "bitand"
            case "|":
                return "bitor"
            case "&&":
                return "and"
            case "||":
                return "or"
            case "^":
                return "xor"
            case "%":
                self.calledfuncs += ["mod"]
                return "mod"
            case "<<":
                self.calledfuncs += ["leftshift"]
                return "<<"
            case ">>":
                self.calledfuncs += ["rightshift"]
                return ">>"
            #intern
            case "ASR":
                return "ASR"
            case "ASL":
                return "ASL"
            case _:
                print("COULD NOT MATCH OPERATION",op)

