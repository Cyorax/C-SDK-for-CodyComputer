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
    
    def generate_temp(self):
        temp = f"_{self.temp_count}"
        self.temp_count += 1
        return temp
        
    def reset_temp_count(self):
        self.temp_count = 0
        
    def add_to_expression_code(self, code):
        self.instructions.append(code)
        
        
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
                self.reset_temp_count()
                expr = self.parse_expression()
                labeltrue = self.create_label()
                labelfalse = self.create_label()
                labelend = self.create_label()
                self.add_to_expression_code(f"if {expr} goto {labeltrue}; else goto {labelfalse};")
                self.add_to_expression_code(f"{labeltrue}:")
                self.tok.eat(")")
                if(self.tok.next() == "{"):
                    self.tok.eat("{")
                    self.parse_instructions()
                    self.tok.eat("}")
                    self.add_to_expression_code(f"goto {labelend};")
                    self.add_to_expression_code(f"{labelfalse}:")
                    if(self.tok.next() == "else"):
                        self.tok.eat("else")
                        self.parse_instruction()
                    self.add_to_expression_code(f"{labelend}:")
                else:
                    self.parse_instruction()
                    self.add_to_expression_code(f"goto {labelend};")
                    self.add_to_expression_code(f"{labelfalse}:")
                    if(self.tok.next() == "else"):
                        self.tok.eat("else")
                        self.parse_instruction()
                    self.add_to_expression_code(f"{labelend}:")
        
            case "for":
                self.tok.eat("for")
                self.tok.eat("(")
                type,ident = self.parse_type()
                self.locals.append(f"{type} {ident};")
                self.tok.eat("=")
                self.reset_temp_count()
                t = self.parse_expression()
                self.add_to_expression_code(f"{ident} = {t};")
                self.tok.eat(";")
                labelwhilecondition = self.create_label()
                labelwhiletrue = self.create_label()
                labelwhilefalse = self.create_label()
                self.add_to_expression_code(labelwhilecondition+":")
                self.reset_temp_count()
                condition = self.parse_expression()
                self.tok.eat(";")
                self.add_to_expression_code(f"if {condition} goto {labelwhiletrue}; else goto {labelwhilefalse};")
                self.add_to_expression_code(labelwhiletrue+":")
                self.reset_temp_count()
                self.parse_assignment()
                self.tok.eat(")")
                if(self.tok.next() == "{"):
                    self.tok.eat("{")
                    self.parse_instructions()
                    self.tok.eat("}")
                    self.add_to_expression_code(f"goto {labelwhilecondition};")
                    self.add_to_expression_code(labelwhilefalse+":")
                else:
                    self.parse_instruction()
                    self.add_to_expression_code(f"goto {labelwhilecondition};")
                    self.add_to_expression_code(labelwhilefalse+":")
                
                
            case "while":
                self.tok.eat("while")
                self.tok.eat("(")
                labelwhilecondition = self.create_label()
                labelwhiletrue = self.create_label()
                labelwhilefalse = self.create_label()
                self.add_to_expression_code(labelwhilecondition+":")
                self.reset_temp_count()
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
                self.reset_temp_count()
                expr = self.parse_expression()
                self.add_to_expression_code(f"return {expr};")
                self.tok.eat(";")
                
            case _:#init, dec, assign oder functioncall
                self.reset_temp_count()
                if self.tok.next() in self.types:
                    type,ident = self.parse_type()
                    
                    self.locals.append(f"{type} {ident};")
                    
                    if(self.tok.next()=="="):
                        self.tok.eat("=")
                        t = self.parse_expression()
                        self.add_to_expression_code(f"{ident} = {t};")
                        
                    
                    while(self.tok.next()==","):
                        self.tok.advance()
                        identlist = self.parse_ident()
                        
                        self.locals.append(f"{type} {identlist};")
                    
                        if(self.tok.next()=="="):
                            self.tok.eat("=")
                            self.reset_temp_count()
                            t = self.parse_expression()
                            self.add_to_expression_code(f"{identlist} = {t};")
                        
                    self.tok.eat(";")
                    
                elif self.tok.next(1) == "(" and self.tok.next() not in ["*","&","++","--"]:
                    self.parse_void_functioncall()
                    self.tok.eat(";")
                    
                elif self.tok.next()!="}":
                    self.parse_assignment()
                    self.tok.eat(";")
    
    def parse_assignment(self):
        left = self.parse_left_unary()
        if(self.tok.next() in ["+=","=","-=","*=","/=","%=","&=","^=","|="]):
            op = self.tok.consume_cur()
            right = self.parse_ternary()
            if(not op.startswith("=")):
                op = op.replace("=","") 
                self.add_to_expression_code(f"{left} = {left} {op} {right};")
            else:
                self.add_to_expression_code(f"{left} = {right};")
        return left
    
        
    def parse_left_add(self):
        left = self.parse_left_mult()
        return self.parse_left_add_strich(left)
    
    def parse_left_add_strich(self, left):
        if self.tok.next() not in ["+", "-"]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_left_mult()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_left_add_strich(t)

    def parse_left_mult(self):
        left = self.parse_left_unary()
        return self.parse_left_mult_strich(left)
    
    def parse_left_mult_strich(self, left):
        if self.tok.next() not in ["*", "/","%"]:
            return left
        op = self.tok.consume_cur()
        right = self.parse_left_unary()
        t = self.generate_temp()
        self.add_to_expression_code(f"{t} = {left} {op} {right};")
        return self.parse_left_mult_strich(t)
    
    def parse_left_unary(self):
        if self.tok.next() in ["*","&","++","--"]:
            tok = self.tok.consume_cur()
            val = self.parse_left_unary()
            t = self.generate_temp()
            if tok == "*":
                return f"*{val}"
            elif tok == "&":
                return f"&{val}"
            elif tok == "++":
                self.add_to_expression_code(f"{val} = {val} + 1;")
                self.add_to_expression_code(f"{t} = {val};")
                return t
            elif tok == "--":
                self.add_to_expression_code(f"{val} = {val} - 1;")
                self.add_to_expression_code(f"{t} = {val};")
                return t
        return self.parse_left_suffix()

    
    def parse_left_suffix(self):
        left = self.parse_left_highest()
        while(self.tok.next() in ["[","++","--"]):
            tok = self.tok.consume_cur()
            t = self.generate_temp()
            match tok:
                case "++":
                    self.add_to_expression_code(f"{left} = {left} + 1;")
                case "--":
                    self.add_to_expression_code(f"{left} = {left} - 1;")
                case "[":
                    expr = self.parse_left_add()
                    self.tok.eat("]")
                    self.add_to_expression_code(f"{t} = {left} + {expr};")
                    left = f"*{t}" 
                case _:
                    pass
        return left
    
    def parse_left_highest(self):
        tok = self.tok.next()
        if tok == "(":
            self.tok.eat("(")
            expr = self.parse_left_add()
            self.tok.eat(")")
            return expr
        if self.tok.is_ident(tok) or self.tok.is_number(tok):
            self.tok.advance()
            return tok
        print(f"COULD NOT PARSE TOKEN {self.tok.next()} in line {self.tok.get_line()}")
    
    
    def parse_expression(self):
        return self.parse_ternary()
    
    def parse_ternary(self):
        condition = self.parse_or()
        if(self.tok.next() == "?"):
            self.tok.eat("?")
            t = self.generate_temp()
            truelabel = self.create_label()
            falselabel = self.create_label()
            endlabel = self.create_label()
            self.add_to_expression_code(f"if {condition} goto {truelabel}; else goto {falselabel};")
            self.add_to_expression_code(f"{truelabel}:")
            left = self.parse_expression()
            self.add_to_expression_code(f"{t} = {left};")
            self.add_to_expression_code(f"goto {endlabel};")
            self.tok.eat(":")
            self.add_to_expression_code(f"{falselabel}:")
            right = self.parse_ternary()
            self.add_to_expression_code(f"{t} = {right};")
            self.add_to_expression_code(f"{endlabel}:")
            condition = t
        return condition
        
    #short circuting ablauf oder:
    # links auswerten
    # if links goto <True>;else goto <Rechts>;
    # <Rechts>:
    #rechts auswerten
    # if rechts goto <True>; else goto <false>;
    # <True>:
    # result = 0;
    # goto <end>;
    # <False>:
    # result = -1; 
    # <end>:
    
    def parse_or(self):
        left = self.parse_and()
        return self.parse_or_strich(left)
    
    def parse_or_strich(self, left):
        if self.tok.next() != "||":
            return left
        self.tok.advance()
        self.tok.advance()
        temp = self.generate_temp()
        result = self.generate_temp()
        truelabel = self.create_label()
        secondlabel = self.create_label()
        falselabel = self.create_label()
        endlabel = self.create_label()
        self.add_to_expression_code(f"{temp} = {left};")
        self.add_to_expression_code(f"if {temp} goto {truelabel}; else goto {secondlabel};")
        self.add_to_expression_code(f"{secondlabel}:")
        right = self.parse_and()
        self.add_to_expression_code(f"{temp} = {right};")
        self.add_to_expression_code(f"if {temp} goto {truelabel}; else goto {falselabel};")
        self.add_to_expression_code(f"{truelabel}:")
        self.add_to_expression_code(f"{result} = 0;")
        self.add_to_expression_code(f"goto {endlabel};")
        self.add_to_expression_code(f"{falselabel}:")
        self.add_to_expression_code(f"{result} = 255;")
        self.add_to_expression_code(f"{endlabel}:")
        return self.parse_or_strich(result)
    
    #short circuting ablauf and:
    # links auswerten
    # if links goto <rechts>;else goto <false>;
    # <Rechts>:
    # rechts auswerten
    # if rechts goto <True>; else goto <false>;
    # <True>:
    # result = 0;
    # goto <end>;
    # <False>:
    # result = 1;
    # <end>:
    
    
    def parse_and(self):
        left = self.parse_bw_or()
        return self.parse_and_strich(left)
    
    def parse_and_strich(self, left):
        if self.tok.next() != "&&":
            return left
        self.tok.advance()
        self.tok.advance()
        temp = self.generate_temp()
        result = self.generate_temp()
        truelabel = self.create_label()
        secondlabel = self.create_label()
        falselabel = self.create_label()
        endlabel = self.create_label()
        self.add_to_expression_code(f"{temp} = {left};")
        self.add_to_expression_code(f"if {temp} goto {secondlabel}; else goto {falselabel};")
        self.add_to_expression_code(f"{secondlabel}:")
        right = self.parse_bw_or()
        self.add_to_expression_code(f"{temp} = {right};")
        self.add_to_expression_code(f"if {temp} goto {truelabel}; else goto {falselabel};")
        self.add_to_expression_code(f"{truelabel}:")
        self.add_to_expression_code(f"{result} = 0;")
        self.add_to_expression_code(f"goto {endlabel};")
        self.add_to_expression_code(f"{falselabel}:")
        self.add_to_expression_code(f"{result} = 255;")
        self.add_to_expression_code(f"{endlabel}:")
        return self.parse_and_strich(result)
    
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
        if self.tok.next() in ["+","-", "!", "*","&","++","--"]:
            tok = self.tok.consume_cur()
            val = self.parse_unary()
            if(tok == "*"):
                return f"{tok} {val}"
            elif(tok == "+"):
                return val
            t = self.generate_temp()
            if(tok == "!"):
                self.add_to_expression_code(f"{t} = {val} == 255;")
            elif(tok == "++"):
                self.add_to_expression_code(f"{val} = {val} + 1;")
                self.add_to_expression_code(f"{t} = {val};")
            elif(tok == "--"):
                self.add_to_expression_code(f"{val} = {val} - 1;")
                self.add_to_expression_code(f"{t} = {val};")
            else:
                self.add_to_expression_code(f"{t} = {tok} {val};")
            return t
        return self.parse_suffix()
    
    def parse_suffix(self):
        left = self.parse_highest()
        while(self.tok.next() in ["--","++","["]):
            tok = self.tok.consume_cur()
            t = self.generate_temp()
            match tok:
                case "++":
                    self.add_to_expression_code(f"{left} = {left} + 1;")
                case "--":
                    self.add_to_expression_code(f"{left} = {left} - 1;")
                case "[":
                    expr = self.parse_expression()
                    self.tok.eat("]")
                    self.add_to_expression_code(f"{t} = {left} + {expr};")
                    left = f"*{t}"
                case _:
                    pass
        return left
    
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
        print(f"COULD NOT PARSE TOKEN {self.tok.next()} in line {self.tok.get_line()}")
        
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
        if(type == "void"):
            print("global variable can't be of type void")
        self.tok.advance()
        int = self.parse_int()
        self.tok.eat(";")
        self.globals.append(f"{type} {ident} = {int};")
        
    def parse_global_dec(self,type,ident):
        if(type == "void"):
            print("global variable can't be of type void")
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

    
        
        
        