### KataArgs (for Python 3.0)

N = -1

def flag(arity = 1, expected_type = None, default = None):
    return (arity, expected_type, default)
    
def make_parser(**schema):
    """Make and return a parser for <schema>.
    
    Flags in the schema are specified with keyword parameters where the key is
    the name of the flag and the value is a tuple containing information about
    arity, expected type and default value.
    
    Doctests have been moved out to README.txt
    """
    
    # Syntax shortcuts
    arity = lambda flag: schema[flag][0]
    expected_type = lambda flag: schema[flag][1]
    default = lambda flag: schema[flag][2]
    
    # Schema validation
    for f in schema.keys():
        if arity(f) != 0 and expected_type(f) is None:
            raise Exception("Schema validation failure: You must specify an expected type for %s." % (f))
            
        if expected_type(f) is not None and \
           expected_type(f).__class__.__name__ != 'type':
            raise Exception("Schema validation failure: Expected type must be a built-in type.")

    def is_flag(v):
        return len(v) > 1 and v[0] == '-'

    def parser(arguments):
        curr = None
        result = {}

        # Default values
        for f in schema.keys():
            if default(f) is not None:
                result[f] = default(f)
                
            elif arity(f) == N:
                result[f] = []
                
        # Parse list of arguments
        for value in arguments:
            if is_flag(value):
                curr = value[1:]
                try:
                    if arity(curr) == 0:
                        result[curr] = True
                        curr = None

                except KeyError:
                    raise Exception("No flag named '%s' have been specified for this parser." % (curr))
                    
            else:
                try:
                    if arity(curr) == N:
                        result[curr].append(expected_type(curr)(value))
                    else:
                        result[curr] = expected_type(curr)(value)
                        
                except KeyError:
                    raise Exception("No flag can be associated with value: %s." % (value))
                
                except ValueError:
                    raise Exception("Expected value of type: %s for flag: %s." % (expected_type(curr), curr))

        return result
        
    return parser
    
if __name__ == '__main__':
    import doctest
    doctest.testfile("kataargs.doctest.txt")

    import sys
    parse = make_parser(l = flag(arity = 0, default = False),
                        p = flag(arity = 1, expected_type = int, default = 0),
                        d = flag(arity = N, expected_type = str, default = None))
    values = parse(sys.argv[1:])
    
    print(values)
