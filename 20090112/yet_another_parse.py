import unittest

class BadSchemaException:
    pass

class Schema:
    def __init__(self, types):
        self.types = types
        self.options = {}
    
    def parse(self, args):
        currOption, currType = None, None
        for arg in args:
            if arg.startswith("-"):
                currOption = arg[1:]
                currType = self.types.get(currOption)
                if currType is bool:
                    self.options[currOption] = True
                elif currType is None:
                    raise BadSchemaException()
            else:
                self.options[currOption] = currType(arg)
        
    def get(self, arg):
        return self.options.get(arg)

class SchemaTest(unittest.TestCase):            
    def testBoolPresent(self):
        s = Schema({ "a" : bool })
        s.parse([ "-a" ])
        self.assertTrue(s.get("a"))
        
    def testBoolAbsent(self):
        s = Schema({ "a" : bool })
        s.parse([ "-a" ])
        self.assertFalse(s.get("b"))
                
    def testString(self):
        s = Schema({ "a" : str })
        s.parse([ "-a", "hello" ])
        self.assertEquals(s.get("a"), "hello")
        
    def testInteger(self):
        s = Schema({ "a" : int })
        s.parse([ "-a", "100" ])
        self.assertEquals(s.get("a"), 100)

    def testMultiArgs(self):
        s = Schema({"a" : int, "b" : bool })
        s.parse([ "-a", "100", "-b" ])
        self.assertEquals(s.get("a"), 100)
        self.assertTrue(s.get("b"))
        
    def testBadSchema(self):
        s = Schema({"a" : int, "b" : bool })
        self.assertRaises(BadSchemaException, s.parse([ "-b", "100", "-c" ]))

        