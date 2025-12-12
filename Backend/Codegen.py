from middleend.GimpleParser import Gimple

##Speichermedien
# globalsmap map: ident -> (offset static, type, initvalue)
# functions list: function
# function map: {Name, lclmaxoffset, localtab , instructions}
# locals map: ident -> (type ,size, offset, location) 
# location string-> {argstack, lclstack}
# instructions list: instruction


## Stackframe exemplarisch, da Stack von 1FF zu 100 geht und SP nur 8 Bit Zahl ist 
#**Hohe Adressen**

# arg...
# arg2
# arg1 byte2
# arg1 byte1
# return addresse byte 2
# return addresse byte 1
# old FBP <-FBP
# loc1 byte2
# loc1 byte1
# loc2
# loc...

#**Niedrige Adressen**


##Memorymap

#0 FBP (Framebasepointer)
#2 Operandenregister 1 Oberes Byte
#3 Operandenregister 1 Unteres Byte
#4 Operandenregister 2 O. Byte
#5 Operandenregister 2 U. Byte
#6 Adresse Datasegment
#7 Adresse Datasegment
#8 ISPTR
#9 ISPTR

# $10-$FF ist Static
# $100-$1FF ist Stack
# $200-$2FF ist Temp

#temp variablen beginnen mit _
# 16 bit Ints werden Simuliert daher butze ich Ram[2] und Ram[3] als Akkumulator 
# Rückgabe über Register 2,3
# littleendian erst das Low byte dann das High byte

class CodeGenerator():
    def __init__(self,Gimple):
        self.gimple = Gimple
        self.finalcode = ["LDA #$FF","STA 0"]
        self.curfunc = {"locals":[]}
        self.init_globalsvalue(Gimple)
        self.compile_Funcs(Gimple)
        
    def init_globalsvalue(self,gimple):
        for g in gimple.globalsmap:
            if str(gimple.globalsmap[g]["value"])!="null":
                self.finalcode += self.assign2(gimple.globalsmap[g]["value"]) + self.write2(g)
        self.finalcode += ["JSR main","JMP BRK"]
        return 
    # label name 
    # n locale Variablen mit 0 initialisieren
    def compile_Funcs(self,instr):
        g = self.gimple
        self.counter = 0
        functions = g.get_Functions()
        for f in functions:
            self.curfunc = f
            #label für Methode
            self.finalcode += [";\t Function: "+f["Name"],f["Name"]+":"]
            # old FBP <-FBP        push EBP     EBP=SP
            overwriteFBP = ["TSX","LDA 0","PHA","TXA","STA 0"]
            self.finalcode += overwriteFBP
            #A = 0
            self.finalcode.append("LDA #0")
            #pushe n mal die 0 aus a 
            for _ in range(0,f["lclmaxoffset"]):
                self.finalcode.append("PHA")
            self.compile_statements(f["Instructions"])
        
        
    def print_final_code(self,filename):
        with open(filename+".asm", "w") as f:
            print(f";   64tass --mw65c02 --nostart -o {filename}.bin {filename}.asm\nADDR= $0300\n.WORD ADDR\n.WORD (ADDR + LAST - FIRST - 1)\n.LOGICAL    ADDR\nFIRST:",file = f)
            for line in self.finalcode:
                print(line, file=f)
            print("BRK: BRA BRK\nLAST\n.ENDLOGICAL",file = f)
        print("OUPUT: "+filename+".asm")
    
    def print_final_code_with_data(self,filename):
        with open(filename+".asm", "w") as f:
            print(f";   64tass --mw65c02 --nostart -o {filename}.bin {filename}.asm\nADDR= $0300\n.WORD ADDR\n.WORD (ADDR + LAST - FIRST - 1)\n.LOGICAL    ADDR\nFIRST:",file = f)
            print(f"LDA #<DATAEXT\nSTA $6\nLDA #>DATAEXT\nSTA $7",file = f)
            for line in self.finalcode:
                print(line, file = f)
            ff = open("data.lib", "r")
            lines = "" 
            for  line in ff:
                lines += line.split("//")[0]
            lines = lines.replace("\n", " ").replace("\t", " ").split()
            print("DATAEXT:",file = f)
            print(".byte $"+", $".join(lines),file = f)
            print("BRK: BRA BRK\nLAST\n.ENDLOGICAL",file = f)
        print("OUPUT: "+filename+".asm")
        
    def compile_statements(self,statementslist):
        if(len(statementslist)==0):
            return
        instr = statementslist[0].split()
        self.finalcode.append(";\t"+" ".join(instr))
        match instr[0]:
            case "if":
                self.compile_if(instr)
            case "return":
                self.compile_return(instr)
            case "assign":
                self.compile_assign(instr)
            case "call":
                self.compile_call(instr)
            case "label":
                self.compile_label(instr)
            case "goto":
                self.compile_goto(instr)
            case "assignret":
                self.compile_assignret(instr)
            case _:
                self.compile_operation(instr)
        
        self.compile_statements(statementslist[1:])
            
    def compile_label(self,instr):
        self.finalcode.append(self.curfunc["Name"]+instr[1]+":")
        
    def compile_goto(self,instr):
        self.finalcode.append("JMP "+self.curfunc["Name"]+instr[1])
    
    # bei Return machen wir also:   also übersetzt
    # Ram[10] = Ram[FBP]            Ram[6] = Ram[$100 + Ram[0]]
    # Sp = FBP                      SP = Ram[0] (weil nur 8 Bit)
    # FBP = Ram[10]                 Ram[0] = Ram[6]
    # rts                           rts
    
    def compile_return(self,instr):
        retopt = []
        if(len(instr)==2):
            retopt = self.assign2(instr[1])
        ret2 = ["LDA 0", "TAX", "DEX", "TXS", "PLA","STA 0", "RTS"]
        self.finalcode += retopt +ret2
        return 
    
    # call main i,x,y  push y push x push i JSR main
    def compile_call(self, instr):
        func = instr[1]
        args = instr[2:]
        call = []
        for a in reversed(args):
            call += self.push_arg(a)
        call.append(f"JSR {func}")
        for _ in range(len(args)):
            call.append("PLA")
            call.append("PLA")
        self.finalcode += call
        return

    #assign dest value -> assign2(value) write2(dest)
    def compile_assign(self,instr):
        self.finalcode += self.assign2(instr[2]) + self.write2(instr[1])
    
    #op dest op1 op2 -> assign2(op1) assign4(op2) op write2(dest)
    def compile_operation(self,instr):
        if(instr[0] == "mult"):
            self.compile_call(["call","mult",instr[2],instr[3]])
            self.compile_assignret(["return",instr[1]])
            return
        elif(instr[0] == "div"):
            self.compile_call(["call","div",instr[2],instr[3]]) 
            self.compile_assignret(["return",instr[1]])
            return
        elif(instr[0] == "mod"):
            self.compile_call(["call","mod",instr[2],instr[3]]) 
            self.compile_assignret(["return",instr[1]])
            return
        elif(instr[0] == "<<"):
            self.compile_call(["call","leftshift",instr[2],instr[3]]) 
            self.compile_assignret(["return",instr[1]])
            return
        elif(instr[0] == ">>"):
            self.compile_call(["call","rightshift",instr[2],instr[3]]) 
            self.compile_assignret(["return",instr[1]])
            return
        self.finalcode += self.assign2(instr[2]) + self.assign4(instr[3]) + self.compile_operator(instr[0]) + self.write2(instr[1])
    
    #assignret dest -> write2(dest)
    def compile_assignret(self,instr):
        self.finalcode +=  self.write2(instr[1])
        
    #if op l1 l2 -> assign2(op) interpret2(l1,l2)
    def compile_if(self,instr):
        self.counter += 1
        self.finalcode += self.assign2(instr[1])+["LDA 2","BNE NOT"+str(self.counter),"JMP "+self.curfunc["Name"]+instr[2],"NOT"+str(self.counter)+":","JMP "+self.curfunc["Name"]+instr[3]]
    
    #gimple erzeugt kein sub immer + - oder + und dann zahl die Negativ ist
    def compile_operator(self,operation):
        match operation:
            case "add":
                return ["LDA 2","CLC","ADC 4","STA 2","LDA 3","ADC 5","STA 3"]
        
            case "sub":
                return ["LDA 4","EOR #$FF","CLC","ADC #1","STA 4","LDA 5","EOR #$FF","ADC #0","STA 5"]+self.compile_operator("add")

            case "bitand":
                return ["LDA 2","AND 4","STA 2","LDA 3","AND 5","STA 3"]
            
            case "bitor": 
                return ["LDA 2","ORA 4","STA 2","LDA 3","ORA 5","STA 3"]
            
            case "xor":
                return ["LDA 2","EOR 4","STA 2","LDA 3","EOR 5","STA 3"]
            #shifts nur für 8 bit short ints 
            case "ASL": 
                self.counter += 1
                return ["ASL 2"]
            
            case "ASR":
                self.counter += 1
                return ["LSR 2"]
            
            case "eq":
                self.counter += 1
                return ["LDA 2","EOR 4","STA 2","LDA 3","EOR 5","ORA 2","STA 2","STA 3","CMP #0","BEQ TRUE"+str(self.counter),"LDA #$FF","STA 2","STA 3","TRUE"+str(self.counter)+":"]
            
            case "neq":
                return self.compile_operator("eq") + ["LDA #$FF","EOR 2","STA 2","LDA #$FF","EOR 3","STA 3"]
            # a > b <=> a - b > 0 <=> 0 > b - a <=> b - a < 0 
            case "gt":
                return  self.compile_operator("lt")
            # a < b <=> a - b < 0 bei LT ist einfach da wir einfach gucken können, ob Sign bit gesetzt ist aber bei gt müssen wir die zwei Register nachprüfen
            case "lt": 
                self.counter += 1
                return self.compile_operator("sub") + ["BMI TRUE"+str(self.counter),"JMP FALSE"+str(self.counter),"TRUE"+str(self.counter)+":","LDA #0","STA 2","JMP END"+str(self.counter),"FALSE"+str(self.counter)+":","LDA #$FF","STA 2","END"+str(self.counter)+":"] 
            # a >= b  <=>  a + 1 > b <=> 0 > b - a - 1 <=> b - a - 1 < 0 daher also Ram[4] - 1
            case "gtq":
                return ["LDA 4","CLC","ADC #1","STA 4","LDA 5","ADC #0","STA 5"] + self.compile_operator("gt")
            # a <= b  <=>  a < b + 1 <=>   
            case "ltq":
                return ["LDA 4","CLC","ADC #1","STA 4","LDA 5","ADC #0","STA 5"] + self.compile_operator("lt")
            
            case _:
                print("UNKNOW OPERATION: "+operation+ " IN METHOD "+self.curfunc["Name"])
                return
            
            
    def write2(self,ident):
        if(ident[0]=="_"):
            return ["LDA 2","STA $2"+str(int(ident[1:])*2).zfill(2),"LDA 3","STA $2"+str(int(ident[1:])*2 + 1).zfill(2)]
        elif(ident[0]=="*"):
            return self.assign4(ident[1:]) + ["LDA #0","TAY","LDA 2","STA (4),Y"]+(["LDA 3","INY","STA (4),Y"] if self.is_two_bytes(ident) else [])
        elif(ident in self.curfunc["locals"]):
            return self.compute_lowBitstackaddress_in_X(ident) + ["LDA 2","STA $100,X"] +(["INX","LDA 3","STA $100,X"] if self.curfunc["locals"][ident]["size"] == 2 else [])
        elif(ident in self.gimple.globalsmap):
            return ["LDA 2","STA "+str(10+self.gimple.globalsmap[ident]["offset"]),"LDA 3","STA "+str(11+self.gimple.globalsmap[ident]["offset"])]
            #return ["LDA $2"+str(int(ident[1:])*2+1).zfill(2),"PHA","LDA $2"+str(int(ident[1:])*2).zfill(2),"PHA"]
        else:
            print("UNKNOW VARIABLE FOUND: "+ident+" IN FUNCTION: "+self.curfunc["Name"])
            
    # HIGHbyte zuerst pushen da stack von oben nach unten für little Endian und args sind immer 16 bit 
    def push_arg(self,ident):
        return self.assign2(ident) + ["LDA 3","PHA","LDA 2","PHA"]
            
    def assign2(self,ident):
        if(ident[0]=="-"):
            return self.assign2(ident[1:]) + ["LDA 2","EOR #$FF","CLC","ADC #1","STA 2","LDA 3","EOR #$FF","ADC #0","STA 3"]
        elif(ident[0]=="_"):
            return ["LDA $2"+str(int(ident[1:])*2).zfill(2),"STA 2","LDA $2"+str(int(ident[1:])*2 + 1).zfill(2),"STA 3"]
        elif(ident[0]=="*"):    # x da die zwei als Akkumulator und aktueller Speicher für den Pointer dient
            return self.assign2(ident[1:]) + ["LDA #0","TAY","LDA (2),Y"]+(["TAX","INY","LDA (2),Y","STA 3","TXA","STA 2"] if self.is_two_bytes(ident) else ["STA 2","LDA #0","STA 3"])
        elif(ident in self.curfunc["locals"]):
            return self.compute_lowBitstackaddress_in_X(ident) + ["LDA $100,X","STA 2"] +(["INX","LDA $100,X","STA 3"] if self.curfunc["locals"][ident]["size"] == 2 else ["LDA #0","STA 3"])
        elif(ident in self.gimple.globalsmap):
            return ["LDA "+str(10+self.gimple.globalsmap[ident]["offset"]),"STA 2","LDA "+str(11+self.gimple.globalsmap[ident]["offset"]),"STA 3"]
        else:
            value = int(ident)
            high = (value >> 8) & 0xFF
            low  = value & 0xFF
            return ["LDA #"+str(low),"STA 2","LDA #"+str(high),"STA 3"]
        return 
    
    def assign4(self,ident):
        if(ident[0]=="-"):
            return self.assign4(ident[1:]) + ["LDA 4","EOR #$FF","CLC","ADC #1","STA 4","LDA 5","EOR #$FF","ADC #0","STA 5"]
        elif(ident[0]=="_"):
            return ["LDA $2"+str(int(ident[1:])*2).zfill(2),"STA 4","LDA $2"+str(int(ident[1:])*2 + 1).zfill(2),"STA 5"]
        elif(ident[0]=="*"):    # x da die zwei als Akkumulator und aktueller Speicher für den Pointer dient
            return self.assign4(ident[1:]) + ["LDA #0","TAY","LDA (4),Y"]+(["TAX","INY","LDA (4),Y","STA 5","TXA","STA 4"] if self.is_two_bytes(ident) else ["STA 4","LDA #0","STA 5"])
        elif(ident in self.curfunc["locals"]):
            return self.compute_lowBitstackaddress_in_X(ident) + ["LDA $100,X","STA 4"] +(["INX","LDA $100,X","STA 5"] if self.curfunc["locals"][ident]["size"] == 2 else ["LDA #0","STA 5"])
        elif(ident in self.gimple.globalsmap):
            return ["LDA "+str(10+self.gimple.globalsmap[ident]["offset"]),"STA 4","LDA "+str(11+self.gimple.globalsmap[ident]["offset"]),"STA 5"]
        else:
            value = int(ident)
            high = (value >> 8) & 0xFF
            low  = value & 0xFF
            return ["LDA #"+str(low),"STA 4","LDA #"+str(high),"STA 5"]
        
    def is_two_bytes(self, ident):
        base = ident.lstrip("*")
        if base in self.curfunc["locals"]:
            return self.curfunc["locals"][base]["type"] != "pointer onebyte"
        if base in self.gimple.globalsmap:
            return self.gimple.globalsmap[base]["type"] != "pointer onebyte"
        return True

    
    #highbit = 1 low = 0 Methode fügt code hinzu zum berechnen der Stackaddressen zur Laufzeit
    def compute_lowBitstackaddress_in_X(self,ident):
        m = self.curfunc["locals"][ident]
        if m["location"] == "arg":
            #Skip FBP + Ret
            return ["LDA 0","CLC","ADC #"+str(m["offset"] + 3),"TAX"]
        else:
            #skip FBP und -1 wegen subtraktion
            return ["LDA 0","CLC","SBC #"+str(m["offset"]-1),"TAX"]
            