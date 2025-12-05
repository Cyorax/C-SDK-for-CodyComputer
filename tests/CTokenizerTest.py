import unittest
from Frontend import CTokenizer


class TestCTokenizer(unittest.TestCase):
    
    def test_doubles(self):
        tok = CTokenizer.Tokenizer(".1 int main(){\n .2 int i=(2==1);\n .3 }")
        self.assertEqual(tok.next(10), "==")