import unittest
from Frontend import CTokenizer


class TestCTokenizer(unittest.TestCase):
    
    def test_doubles(self):
        tok = CTokenizer.Tokenizer(".1 int main(){\n .2 int i=(2==1);\n .3 }",fromfile=False)
        self.assertEqual(tok.next(10), "==")
        
    def test_linenumbers(self):
        tok = CTokenizer.Tokenizer(".1 int main(){\n .2 int i=(2==1);\n .3 }",fromfile=False)
        items = [tok.next(x) for x in range(8)]
        self.assertEqual(items, ["int","main","(",")","{","int","i","="])
        
    def test_EOF(self):
        tok = CTokenizer.Tokenizer(".1 int public()",fromfile=False)
        self.assertEqual(tok.next(4), "EOF")
        
    def test_next(self):
        tok = CTokenizer.Tokenizer(".1 int public()",fromfile=False)
        self.assertEqual(tok.next(3), ")")
    
    def test_consume_cur(self):
        tok = CTokenizer.Tokenizer(".1 int public()",fromfile=False)
        self.assertEqual(tok.consume_cur(), "int")
        self.assertEqual(tok.consume_cur(), "public")
        
    def test_single_vs_double(self):
        tok = CTokenizer.Tokenizer("a<=b!=c>d=f", fromfile=False)
        items = [tok.consume_cur() for _ in range(9)]
        self.assertEqual(items,["a","<=","b","!=","c",">","d","=","f"])
    
    def test_double_nex(self):
        tok = CTokenizer.Tokenizer("!=", fromfile=False)
        self.assertEqual(tok.next(),"!=")
        
    def test_while(self):
        tok = CTokenizer.Tokenizer("while(x){x=x+1;}", fromfile=False)
        self.assertEqual(tok.get_tokens(),["while","(","x",")","{","x","=","x","+","1",";","}"])

    def test_if(self):
        tok = CTokenizer.Tokenizer("if(a)b=1;else b=2;", fromfile=False)
        self.assertEqual(tok.get_tokens(),["if","(","a",")","b","=","1",";","else","b","=","2",";"])

    def test_expression(self):
        tok = CTokenizer.Tokenizer("a=(b+3)*c;", fromfile=False)
        self.assertEqual(tok.get_tokens(),["a","=","(","b","+","3",")","*","c",";"])



if __name__ == "__main__":
    unittest.main()