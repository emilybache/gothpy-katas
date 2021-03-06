### KataArgs (for Python 3.0)

def flag(expected_type, default = None):
    if expected_type is None:
        return (0, expected_type, False)

    elif type(expected_type) == list:
        if len(expected_type) > 1:
            raise Exception("You cannot specify more than one type for a list.")

        return (-1, expected_type[0], default)

    else:
        return (1, expected_type, default)
    
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
        if expected_type(f) is not None and \
           expected_type(f).__class__.__name__ != 'type':
            raise Exception("Expected type must be a built-in type.")

    def is_flag(v):
        return len(v) > 1 and v[0] == '-'

    def parser(arguments):
        curr = None
        result = {}

        # Default values
        for f in schema.keys():
            if default(f) is not None:
                result[f] = default(f)
                
            elif arity(f) == -1:
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
                    if arity(curr) == -1:
                        if "," in value:
                            values = value.split(",")
                        else:
                            values = [value,]

                        for v in values:
                            result[curr].append(expected_type(curr)(v))

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
    doctest.testfile("README.txt")

    import sys
    parse = make_parser(l = flag(None),
                        p = flag(int, default = 0),
                        d = flag([str], default = None))
    values = parse(sys.argv[1:])
    
    print(values)
