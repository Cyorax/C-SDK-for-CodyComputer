import unittest
from Frontend import GimpleParser, GimpleTokenizer
from Backend import Optimizer


class TestGimple(unittest.TestCase):
    
    def test_DCE(self):
        tok = GimpleTokenizer.Tokenizer("int global1 = 100;int main(){int local1; local1 = 10; abc(local1);} short int abc(int i){ return 0;} int* bca(){ return 0;}")
        gim = GimpleParser.Gimple(tok)
        op = Optimizer.Optimizer(gim)
        self.assertEqual(op.availablefuncs, ["main","abc"])
        
        
if __name__ == "__main__":
    unittest.main()