#todos in files der priorität nach

#todos codegen:
# Operatoren fixen (||,&&,>=,>,>>,<<) & als adressengetter 

#todos CParser:
# else for und dec von mehrereren Variablen

#todos CTokenizer:
# multiline commands

#todos libs:
# codygrapics bitmapped, sprites, scrolling, codykeyboard, Sound (in der Uni testen)

#todos CParser:
#Typechecking

#todos Preprozessor:
# makros

from Frontend import CTokenizer
from Frontend import Preprozessor
from sys import argv
from Frontend import CParser
from middleend import GimpleTokenizer
from middleend import GimpleParser
from Backend import Optimizer
from Backend.Codegen import CodeGenerator

#Verwendung python main.py -op1 -op2 outputname cfile1 cfile2 ...

if(len(argv) == 0):
    print("false usage")
    exit(0)

options = []
opt_pntr = 1
while(argv[opt_pntr].startswith("-")):
    options.append(argv[opt_pntr])
    opt_pntr += 1

outputname = argv[opt_pntr]
syslibs = []
tok = CTokenizer.Tokenizer(argv[opt_pntr+1])
opt_pntr += 2
pre = Preprozessor.Preprozessor(tok)
cpar = CParser.CParser(tok)
syslibs += pre.get_syslibs()
gimptok = GimpleTokenizer.Tokenizer(" ".join(cpar.generate_gimple()))
gim = GimpleParser.Gimple(gimptok)

while(opt_pntr < len(argv)):
    tok1 = CTokenizer.Tokenizer(argv[opt_pntr])
    opt_pntr += 1
    pre1 = Preprozessor.Preprozessor(tok1)
    cpar1 = CParser.CParser(tok1)
    syslibs += pre1.get_syslibs()
    gimptok1 = GimpleTokenizer.Tokenizer(" ".join(cpar1.generate_gimple()))
    gim1 = GimpleParser.Gimple(gimptok1)
    gim.merge(gim1)
    
syslibs = set(syslibs)
for lib in syslibs:
    f = open("lib/"+lib.replace(".h",".gimple"), "r")
    lines = "" 
    for  line in f:
        lines += line.split("//")[0]
    gimptok2 = GimpleTokenizer.Tokenizer(lines)
    gim2 = GimpleParser.Gimple(gimptok2)
    gim.merge(gim2)
    
opt = Optimizer.Optimizer(gim);
gim.dump_gimple()
c = CodeGenerator(gim)
c.print_final_code(outputname)

