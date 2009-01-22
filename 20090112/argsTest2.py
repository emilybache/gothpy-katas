import unittest

from args2 import *

class ArgsTest(unittest.TestCase):
    
    def hidtest_split_options(self):
        args = Args()
        g = args.split_options(["-l", "-i", "hello", "why", "-f"])
        option, values = next(g)
        self.assertEqual(option, 'l')
        self.assertEqual(values, [])
        option, values = next(g)
        self.assertEqual(option, 'i')
        self.assertEqual(values, ["hello", "why"])
        option, values = next(g)
        self.assertEqual(option, 'f')
        self.assertEqual(values, [])

                
    
    def test_noargs(self):
        args = Args()
        self.assertTrue(args.parse([]))
        
    def test_boolean(self):
        args = Args(l=bool)
        args.parse(["-l"])
        self.assertTrue(args.l)

    def test_int(self):
        args = Args(i=int)
        args.parse(["-i", "10"])
        self.assertEqual(args.i, 10)
        
    def test_float(self):
        args = Args(f=float)
        args.parse(["-f", "10.0"])
        self.assertEqual(args.f, 10.0)

    def test_str(self):
        args = Args(s=str)
        args.parse(["-s", "hello"])
        self.assertEqual(args.s, "hello")

    def test_float_and_str(self):
        args = Args(f=float, s=str)
        args.parse(["-s", "hello", "-f", "10.0"])
        self.assertEqual(args.f, 10.0)
        self.assertEqual(args.s, "hello")

    def test_str_and_float(self):
        args = Args(f=float, s=str)
        args.parse(["-f", "10.0", "-s", "hello"])
        self.assertEqual(args.f, 10.0)
        self.assertEqual(args.s, "hello")
        
    def test_str_and_bool_and_float(self):
        args = Args(f=float, b=bool, s=str)
        args.parse(["-b", "-f", "10.0", "-s", "hello"])
        self.assertEqual(args.f, 10.0)
        self.assertEqual(args.s, "hello")
        self.assertEqual(args.b, True)
    
    def test_missing_bool(self):
        args = Args(b=bool)
        args.parse([])
        self.assertEqual(args.b, False)
        
    def test_list(self):
        args = Args(l=[str])
        args.parse(["-l", "this", "should", "be", "a", "list"])
        self.assertEqual(["this", "should", "be", "a", "list"], args.l)

unittest.main()
