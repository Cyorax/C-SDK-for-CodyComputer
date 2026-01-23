import unittest
from middleend import DACParser
from middleend import DACTokenizer
from Backend import Optimizer


class Testdac(unittest.TestCase):
    
    def test_DCE(self):
        tok = DACTokenizer.Tokenizer("int global1 = 100;int main(){int local1; local1 = 10; abc(local1);} short int abc(int i){ return 0;} int* bca(){ return 0;}")
        gim = DACParser.DAC(tok)
        op = Optimizer.Optimizer(gim)
        self.assertEqual(op.availablefuncs, ["main","abc"])
    
    def test_constant_folding1(self):
        tok = DACTokenizer.Tokenizer("int global1 = 100;int main(){int local1; local1 = 10; abc(local1);} short int abc(int i){ return 0;} int* bca(){ return 0;}")
        gim = DACParser.DAC(tok)
        op = Optimizer.Optimizer(gim)
        op.constant_folding()
        print(gim.get_Functions()["main"])
        
if __name__ == "__main__":
    unittest.main()