#todos in files der priorität nach

#todos libs:
# scrolling, Sound (in der Uni testen) 

#todos CParser:
#Typechecking , Scopes,

#todos Preprozessor:
# makros

from Frontend import CTokenizer
from Frontend import Preprozessor
from sys import argv
from Frontend import CParser
from middleend import DACTokenizer
from middleend import DACParser
from Backend import Optimizer
from Backend.Codegen import CodeGenerator

#Verwendung python main.py -op1 -op2 outputname cfile1 cfile2 ...

if(len(argv) == 0):
    print("false usage")
    exit(0)

options = []
opt_pntr = 1
while(argv[opt_pntr].startswith("-")):
    options.append(argv[opt_pntr].replace("-",""))
    opt_pntr += 1

outputname = argv[opt_pntr]
syslibs = []
tok = CTokenizer.Tokenizer(argv[opt_pntr+1])
opt_pntr += 2
pre = Preprozessor.Preprozessor(tok)
cpar = CParser.CParser(tok)
syslibs += pre.get_syslibs()
gimptok = DACTokenizer.Tokenizer(" ".join(cpar.generate_gimple()))
gim = DACParser.DAC(gimptok)
 
while(opt_pntr < len(argv)):
    tok1 = CTokenizer.Tokenizer(argv[opt_pntr])
    opt_pntr += 1
    pre1 = Preprozessor.Preprozessor(tok1)  
    cpar1 = CParser.CParser(tok1)
    syslibs += pre1.get_syslibs()
    gimptok1 = DACTokenizer.Tokenizer(" ".join(cpar1.generate_gimple()))
    gim1 = DACParser.DAC(gimptok1)
    gim.merge(gim1)
    
syslibs = set(syslibs)
for lib in syslibs:
    f = open("lib/"+lib.replace(".h",".dac"), "r")
    lines = "" 
    for  line in f:
        lines += line.split("//")[0]
    gimptok2 = DACTokenizer.Tokenizer(lines)
    gim2 = DACParser.DAC(gimptok2)
    gim.merge(gim2)

opt = Optimizer.Optimizer(gim);
if("gimple" in options):
    with open(outputname+".dac", "w") as f:
        for line in cpar.generate_gimple():
            print(line, file=f)
            
if("precomp" in options):
    gim.dump_gimple()
    
c = CodeGenerator(gim)
if("data" in options):
    c.print_final_code_with_data(outputname)
else:
    c.print_final_code(outputname)

