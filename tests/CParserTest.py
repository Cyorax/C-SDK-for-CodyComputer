import unittest
from Frontend import CTokenizer, CParser

class TestCParser(unittest.TestCase):
    
    def test_mutiple_inits_and_decs_oneline(self):
        tok = CTokenizer.Tokenizer(".1 int main() {\n .2 int a =2*acdc(),b,c=187 + acdc(),d;}\n",fromfile=False)
        par = CParser.CParser(tok)
        self.assertEqual(par.generate_dac(),['int main(){', 'int a;', 'int b;', 'int c;', 'int d;', '_0 = acdc();', '_1 = 2 * _0;', 'a = _1;', '_0 = acdc();', '_1 = 187 + _0;', 'c = _1;', '}'])
    
    def test_arragement(self):
        tok = CTokenizer.Tokenizer(".1 int main() {\n .2 int c,d; \n .3 c = d; .4 int a,b; }\n",fromfile=False)
        par = CParser.CParser(tok)
        self.assertEqual(par.generate_dac(),['int main(){', 'int c;', 'int d;', 'int a;', 'int b;', 'c = d;', '}'])
    
    def test_while(self):
        tok = CTokenizer.Tokenizer(".1 int main() {\n .2 int c,d; \n .3 while(c == d){ } }\n",fromfile=False)
        par = CParser.CParser(tok)
        self.assertEqual(par.generate_dac(),['int main(){', 'int c;', 'int d;', '<c.1>:', '_0 = c == d;', 'if _0 goto <c.2>; else goto <c.3>;', '<c.2>:', 'goto <c.1>;', '<c.3>:', '}'])
    
    def test_if(self):
        tok = CTokenizer.Tokenizer(".1 int main() {\n .2 int c,d; \n .3 if(c == d){ c=1; }else if (c < d){ c = 0;}else{c=2;} }\n",fromfile=False)
        par = CParser.CParser(tok)
        self.assertEqual(par.generate_dac(),['int main(){', 'int c;', 'int d;', '_0 = c == d;', 'if _0 goto <c.1>; else goto <c.2>;', '<c.1>:', 'c = 1;', 'goto <c.3>;', '<c.2>:', '_0 = c < d;', 'if _0 goto <c.4>; else goto <c.5>;', '<c.4>:', 'c = 0;', 'goto <c.6>;', '<c.5>:', 'c = 2;', '<c.6>:', '<c.3>:', '}'])
     
  
    def test_precedence_mult_add(self):
        tok = CTokenizer.Tokenizer(".1 int main() {\n .2 int a,b,c,d; \n .3 a = b + c * d; }\n",fromfile=False)
        par = CParser.CParser(tok)
        self.assertEqual(par.generate_dac(),['int main(){', 'int a;', 'int b;', 'int c;', 'int d;', '_0 = c * d;', '_1 = b + _0;', 'a = _1;', '}'])
