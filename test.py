from interpreter import *
import unittest

class TestInterpreter(unittest.TestCase):
    def test_math(self):
        print('1 + 1 = 2')
        expr1 = tAdd(tInt(1), tInt(1))
        self.assertEqual(evaluate(expr1), 2)

        print('1 - 2 = -1')
        expr2 = tSub(tInt(1), tInt(2))
        self.assertEqual(evaluate(expr2), -1)
        
        print('2 * 2 = 4')
        expr3 = tMul(tInt(2), tInt(2))
        self.assertEqual(evaluate(expr3), 4)
        
        print('6 / 3 = 2')
        expr4 = tDiv(tInt(6), tInt(3))
        self.assertEqual(evaluate(expr4), 2)
    
    def test_compare (self):
        print('1 < 2 = True')
        expr1 = tLt(tInt(1), tInt(2))
        self.assertEqual(evaluate(expr1), True)

        print('2 > 1 = True')
        expr2 = tGt(tInt(2), tInt(1))
        self.assertEqual(evaluate(expr2), True)
        
        print('1 <= 1 = True')
        expr3 = tLte(tInt(1), tInt(1))
        self.assertEqual(evaluate(expr3), True)
        
        print('1 >= 1 = True')
        expr4 = tGte(tInt(1), tInt(1))
        self.assertEqual(evaluate(expr4), True)
        
    def test_assign_and_Ident(self):
        print('{a = 100; a} = 100')
        expr1 = Sequence([tAs('a', tInt(100)), tId('a')])
        self.assertEqual(evaluate(expr1), 100)
        
        print('{a = 100; b = a + 1; b} = 101')
        expr2 = Sequence([tAs('a', tInt(100)), tAs('b', tAdd(tId('a'), tInt(1))), tId('b')])
        self.assertEqual(evaluate(expr2), 101)
        
    def test_if(self):
        print('if(1 > 2), 2 else 1) == 1')
        expr1 = If(tGt(tInt(1), tInt(2)), tInt(2), tInt(1))
        self.assertEqual(evaluate(expr1), 1)
        
    def test_while(self):
        print('i = 0; while(i < 10), i = i + 1; i) == 10')
        expr1 = Sequence([tAs('i', tInt(0)), While(tLt(tId('i'), tInt(10)), tAs('i', tAdd(tId('i'), tInt(1)))), tId('i')])
        self.assertEqual(evaluate(expr1), 10)
        
    def test_function(self):
        print('def add(a + b) { return a + b }, add(1, 2) == 3')
        program1 = Program([Function('add', ['a', 'b'], tAdd(tId('a'), tId('b')))],[Call('add', [tInt(1), tInt(2)])])
        self.assertEqual(eval_program(program1), 3)
                
if __name__ == '__main__':
    unittest.main()
