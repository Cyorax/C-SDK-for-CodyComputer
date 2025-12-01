import unittest
from middleend import GimpleParser
from middleend import GimpleTokenizer


class TestGimple(unittest.TestCase):
    
    def test_globals(self):
        tok = GimpleTokenizer.Tokenizer("int global1 = 100;int main (){ }")
        gim = GimpleParser.Gimple(tok)
        self.assertEqual(len(gim.globalsmap), 1)
        
    def test_locals(self):
        tok = GimpleTokenizer.Tokenizer("int global1 = 100;int main(){int local1; }")
        gim = GimpleParser.Gimple(tok)
        self.assertEqual(len(gim.functions[0]["locals"]), 1)
        
if __name__ == "__main__":
    unittest.main()