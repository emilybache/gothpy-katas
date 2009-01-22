import unittest

from args import *

class ArgsTest(unittest.TestCase):
    def test_NoArgsNotValid(self):
        args = Args({})
        self.failIf(args.is_valid())
    def test_NoArgsIsEmpty(self):
        args = Args({})
        args.parse([])
        self.failUnless(args.is_valid())
    def test_boolean(self):
        args = Args({"l" : bool})
        args.parse(["-l"])
        self.failUnless(args.is_valid())
        self.failUnlessEqual(True, args["l"])
    def test_not_matching_schema(self):
        args = Args({})
        try:
            args.parse(["-l"])
            self.fail("should have thrown bad args exception")
        except BadArgsException:
            self.failUnlessEqual(False, args.is_valid())
    def test_integer(self):
        args = Args({"p" : int})
        args.parse(["-p", "8080"])
        self.failUnless(args.is_valid())
        self.failUnlessEqual(8080, args["p"])
    def test_missing_boolean(self):
        args = Args({"l" : bool})
        args.parse([])
        self.failUnless(args.is_valid())
        self.failUnlessEqual(False, args["l"])
        
    def test_string(self):
        args = Args({"d" : str})
        args.parse(["-d", "/usr/stuff"])
        self.failUnless(args.is_valid())
        self.failUnlessEqual("/usr/stuff", args["d"])
        
    def test_wrong_type(self):
        args = Args({"d" : int})
        try:
            args.parse(["-d", "/usr/stuff"])
            self.fail("should have thrown bad args exception")
        except BadArgsException:
            self.failUnlessEqual(False, args.is_valid())
    def test_str_array(self):
        args = Args({"a" : list})
        args.parse(["-a", "one", "thing", "at", "a", "time"])
        self.failUnlessEqual(["one", "thing", "at", "a", "time"], args["a"])
        
    def test_int_array(self):
        args = Args({"a" : int_list})
        args.parse(["-a", "1", "2", "3"])
        self.failUnlessEqual([1, 2, 3], args["a"])
unittest.main()