import unittest
from middleend import DACParser
from middleend import DACTokenizer


class TestGimple(unittest.TestCase):
    
    def test_globals(self):
        tok = DACTokenizer.Tokenizer("int global1 = 100;int main (){ }")
        gim = DACParser.DAC(tok)
        self.assertEqual(len(gim.globalsmap), 1)
        
    def test_locals(self):
        tok = DACTokenizer.Tokenizer("int global1 = 100;int main(){int local1; }")
        gim = DACParser.DAC(tok)
        self.assertEqual(len(gim.functions[0]["locals"]), 1)
        
if __name__ == "__main__":
    unittest.main()