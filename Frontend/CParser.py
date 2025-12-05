from Frontend.CTokenizer import Tokenizer

class CParser:

    def __init__(self, tok):
        self.tok = tok
        self.final_code = []
        self.globals = []
        self.functions = {}
        self.controllstrukturencounter = 0;
        self.types = ["char","int","short","void"]
        self.parse()

    def create_label(self):
        self.controllstrukturencounter += 1
        return "<c."+str(self.controllstrukturencounter)+">"
    
    def generate_gimple(self):
        return self.globals+self.final_code
        
        
    def parse(self):
        if(self.tok.next() == "EOF"):
            return 
        type,ident = self.parse_type()
        match self.tok.next():
            case "=":
                self.parse_global_init(type,ident)
            case ";":
                self.parse_global_dec(type,ident)
            case _:
                functionhead = self.parse_function(type,ident)
                if(functionhead is not None):
                    self.final_code += [functionhead] + self.locals + self.instructions + ["}"]
        self.parse()
        
    def parse_function(self,type,ident):
        self.tok.curfunc = ident
        self.tok.eat("(")
        args = ""
        argscounter = 0
        argtypesordered = []
        if(self.tok.next() == "void"):
            self.tok.advance()
        while(self.tok.next()!=")"):
            argtype, argident = self.parse_type()
            args += argtype+" "+argident
            argscounter += 1;
            argtypesordered += [argtype]
            if(self.tok.next() == ","):
                self.tok.advance()
                args += ","
        self.tok.eat(")")
        if(self.tok.next() == ";"):
            self.tok.eat(";")
            self.functions[ident]={"type":type,"argcount":argscounter,"argtypes":argtypesordered}
            return None
        else:
            self.functions[ident]={"type":type,"argcount":argscounter,"argtypes":argtypesordered}
            self.locals = []
            self.instructions = []
            self.temp_count = 0
            self.tok.eat("{")
            self.parse_functionbody()
            self.tok.eat("}")
            return f"{type} {ident}({args})"+"{"
        
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
                expr = self.parse_expression()
                labeltrue = self.create_label()
                labelfalse = self.create_label()
                self.add_to_expression_code(f"if {expr} goto {labeltrue}; else goto {labelfalse}")
                self.add_to_expression_code(f"{labeltrue}:")
                self.tok.eat(")")
                if(self.tok.next() == "{"):
                    self.tok.eat("{")
                    self.parse_instructions()
                    self.tok.eat("}")
                    self.add_to_expression_code(f"{labelfalse}:")
                    #hier else
                else:
                    self.parse_instruction()
                    self.add_to_expression_code(f"{labelfalse}:")
                    #hier else
                
                
            case "while":
                self.tok.eat("while")
                self.tok.eat("(")
                labelwhilecondition = self.create_label()
                labelwhiletrue = self.create_label()
                labelwhilefalse = self.create_label()
                self.add_to_expression_code(labelwhilecondition+":")
                expr = self.parse_expression()
                self.add_to_expression_code(f"if {expr} goto {labelwhiletrue}; else goto {labelwhilefalse};")
                self.tok.eat(")")
                if(self.tok.next() == "{"):
                    self.tok.eat("{")
                    self.add_to_expression_code(labelwhiletrue+":")
                    self.parse_instructions()
                    self.tok.eat("}")
                    self.add_to_expression_code(f"goto {labelwhilecondition};")
                    self.add_to_expression_code(labelwhilefalse+":")
                else:
                    self.parse_instruction()
                    self.add_to_expression_code(f"goto {labelwhilecondition};")
                    self.add_to_expression_code(labelwhilefalse+":")
                 
            
            case "return":
                self.tok.eat("return")
                if(self.tok.next() == ";"):
                    self.tok.eat(";")
                    self.add_to_expression_code("return;")
                expr = self.parse_expression()
                self.add_to_expression_code(f"return {expr};")
                self.tok.eat(";")
                
            case _:#init, dec, assign oder functioncall
                if self.tok.next() in self.types:
                    type,ident = self.parse_type()
                    if(self.tok.next()=="="):
                        self.tok.eat("=")
                        t = self.parse_expression()
                        self.add_to_expression_code(f"{ident} = {t};")
                        self.tok.eat(";")
                    elif(self.tok.next()==";"):
                        self.tok.eat(";")
                    self.locals.append(f"{type} {ident};")
                    
                elif self.tok.next(1) == "(":
                    self.parse_void_functioncall()
                    self.tok.eat(";")
                    
                elif self.tok.next()!="}":
                    op = self.parse_operand()
                    self.tok.eat("=")
                    exp = self.parse_expression()
                    self.add_to_expression_code(f"{op} = {exp};")
                    self.tok.eat(";")
            
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
        
    def parse_expression(self):
        return self.parse_or()
    
    def generate_temp(self):
        temp = f"_{self.temp_count}"
        self.temp_count += 1
        return temp
        
    def add_to_expression_code(self, code):
        self.instructions.append(code)
        
    #operatoren liste :
    # &&,&,||,|,<=,>=,<,>,==,!=,^,+,-,/,*,%,>>,<< und bindet stärker als oder und dazwischen ist xor
    #unär: 
    # - ! 
    
    def parse_or(self):
        left = self.parse_and()
        return self.parse_or_strich(left)
    
    def parse_or_strich(self, left):
        if self.tok.next() != "||":
            return left
        self.tok.advance()
        right = self.parse_and()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} || {right};")
        return self.parse_or_strich(t)
    
    def parse_and(self):
        left = self.parse_bw_or()
        return self.parse_and_strich(left)
    
    def parse_and_strich(self, left):
        if self.tok.next() != "&&":
            return left
        self.tok.advance()
        right = self.parse_bw_or()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} && {right};")
        return self.parse_and_strich(t)
    
    def parse_bw_or(self):
        left = self.parse_bw_xor()
        return self.parse_bw_or_strich(left)
    
    def parse_bw_or_strich(self, left):
        if self.tok.next() != "|":
            return left
        self.tok.advance()
        right = self.parse_bw_xor()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} | {right};")
        return self.parse_bw_or_strich(t)
    
    def parse_bw_xor(self):
        left = self.parse_bw_and()
        return self.parse_bw_xor_strich(left)
    
    def parse_bw_xor_strich(self, left):
        if self.tok.next() != "^":
            return left
        self.tok.advance()
        right = self.parse_bw_and()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} ^ {right};")
        return self.parse_bw_xor_strich(t)

    def parse_bw_and(self):
        left = self.parse_eq()
        return self.parse_bw_and_strich(left)
    
    def parse_bw_and_strich(self, left):
        if self.tok.next() != "&":
            return left
        self.tok.advance()
        right = self.parse_eq()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} & {right};")
        return self.parse_bw_and_strich(t)
    
    def parse_eq(self):
        left = self.parse_cond()
        return self.parse_eq_strich(left)
    
    def parse_eq_strich(self, left):
        if self.tok.next() not in ["==", "!="]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_cond()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_eq_strich(t)
    
    def parse_cond(self):
        left = self.parse_shift()
        return self.parse_cond_strich(left)
    
    def parse_cond_strich(self, left):
        if self.tok.next() not in ["<", ">","<=",">="]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_shift()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_cond_strich(t)
    
    def parse_shift(self):
        left = self.parse_add()
        return self.parse_shift_strich(left)
    
    def parse_shift_strich(self, left):
        if self.tok.next() not in ["<<", ">>"]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_add()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_shift_strich(t)
    
    def parse_add(self):
        left = self.parse_mult()
        return self.parse_add_strich(left)
    
    def parse_add_strich(self, left):
        if self.tok.next() not in ["+", "-"]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_mult()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_add_strich(t)

    def parse_mult(self):
        left = self.parse_unary()
        return self.parse_mult_strich(left)
    
    def parse_mult_strich(self, left):
        if self.tok.next() not in ["*", "/","%"]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_unary()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_mult_strich(t)
    
    def parse_unary(self):
        if self.tok.next() in ["-", "!", "+","*","&"]:
            tok = self.tok.consume_cur()
            val = self.parse_unary()
            t = self.generate_temp()
            self.add_to_expression_code(f"{t} = {tok} {val};")
            return t
        return self.parse_highest()

    def parse_highest(self):
        tok = self.tok.next()
        if tok == "(":
            self.tok.eat("(")
            expr = self.parse_expression()
            self.tok.eat(")")
            return expr
        if self.tok.next(1) == "(":
            return self.parse_functioncall()
        if self.tok.is_ident(tok) or self.tok.is_number(tok) or self.tok.is_character(tok):
            self.tok.advance()
            return tok
        
    def parse_functioncall(self):
        name = self.tok.consume_cur()
        self.tok.eat("(")
        args = []
        while self.tok.next() != ")":
            arg = self.parse_expression()
            args.append(arg)
            if self.tok.next() == ",":
                self.tok.eat(",")
        
        if(name not in self.functions):
            print(f"insuficient functiondeclaration of function {name} in line {self.tok.get_line()}")
        elif(self.functions[name]["type"] == "void"):
            print(f"function of name {name} has returntype void in line {self.tok.get_line()}")
        elif(len(args) != self.functions[name]["argcount"]):
            c = self.functions[name]["argcount"]
            print(f"function of name {name} expected {c} args but only recieved {len(args)} in line {self.tok.get_line()}")
        self.tok.eat(")")
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {name}({', '.join(args)});")
        return t
    
    def parse_void_functioncall(self):
        name = self.tok.consume_cur()
        self.tok.eat("(")
        args = []
        while self.tok.next() != ")":
            arg = self.parse_expression()
            args.append(arg)
            if self.tok.next() == ",":
                self.tok.eat(",")
        
        if(name not in self.functions):
            print(f"insuficient functiondeclaration of function {name} in line {self.tok.get_line()}")
            
        elif(len(args) != self.functions[name]["argcount"]):
            c = self.functions[name]["argcount"]
            print(f"function of name {name} expected {c} args but only recieved {len(args)} in line {self.tok.get_line()}")
        
        self.tok.eat(")")
        self.add_to_expression_code(f"{name}({', '.join(args)});")

    def parse_global_init(self,type,ident):
        self.tok.advance()
        int = self.parse_int()
        self.tok.eat(";")
        self.globals.append(f"{type} {ident} = {int};")
        
    def parse_global_dec(self,type,ident):
        self.tok.advance()
        self.globals.append(f"{type} {ident};")
        
    def parse_type(self):
        type = self.tok.consume_cur()
        while(self.tok.next() == "*"):
            type += self.tok.consume_cur()
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

    
        
        
        