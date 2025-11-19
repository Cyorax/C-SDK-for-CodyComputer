from Frontend.GimpleTokenizer import Tokenizer
from Frontend.GimpleParser import Gimple
from Backend.Codegen import CodeGenerator
from Backend.Optimizer import Optimizer
from sys import argv

# aufruf make outputfilename input1.c input2.c ...

outputname = argv[1]
f = open(argv[2], "r")
lines = ""
for  line in f:
    lines += line.split("//")[0]
tok = Tokenizer(lines)
gim = Gimple(tok)
        
for i in range(3,len(argv)):
    f = open(argv[i], "r")
    lines = ""
    for  line in f:
        lines += line.split("//")[0]
    toke = Tokenizer(lines)
    gimple = Gimple(toke)
    gim.merge(gimple)


opt = Optimizer(gim)
gim.dump_gimple()
c = CodeGenerator(gim)
c.print_final_code(outputname)

