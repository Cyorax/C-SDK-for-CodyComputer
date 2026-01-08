import unittest
from middleend import DACTokenizer


class TestGimple(unittest.TestCase):
    
    def test_EOF(self):
        tok = DACTokenizer.Tokenizer("int public()")
        self.assertEqual(tok.next(4), "EOF")
        
    def test_nex(self):
        tok = DACTokenizer.Tokenizer("int public()")
        self.assertEqual(tok.next(3), ")")
    
    def test_consume_cur(self):
        tok = DACTokenizer.Tokenizer("int public()")
        self.assertEqual(tok.consume_cur(), "int")
        self.assertEqual(tok.consume_cur(), "public")
    
    def test_tokenize(self):
        tok = DACTokenizer.Tokenizer("int public()")
        self.assertEqual(tok.get_tokens(),["int","public","(",")"])
    
if __name__ == "__main__":
    unittest.main()
