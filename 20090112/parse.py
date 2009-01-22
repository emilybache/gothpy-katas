import sys, doctest


class Parser:

    """
    >>> p = Parser(l=bool)
    >>> p(['-l'])
    {'l': True}
    >>> p([])
    {'l': False}
    
    >>> p = Parser(i=int)
    >>> p(['-i','8080']) == dict(i=8080)
    True
    
    >>> p = Parser(l=bool,i=int,s=str)
    >>> p(['-l','-s','foo','-i','8080']) == dict(l=True,i=8080,s='foo')
    True
    
    >>> p = Parser(l=bool,i=int,s=str,f=float)
    >>> p(['-l','-s','foo','-i','8080','-f',1.23]) == dict(l=True,i=8080,s='foo',f=1.23)
    True
    
    >>> p = Parser(l=bool,i=int,s=str)
    >>> p(['-l','-s','foo','-i','8080','-k'])
    Traceback (most recent call last):
    ...
    KeyError: 'k'
    
    
    >>> p = Parser(l=bool,i=int,s=str)
    >>> p(['-l','-s','foo'])
    Traceback (most recent call last):
    ...
    KeyError

    """
    def __init__(self, **kw):
        self.schema = kw
   
    def __call__(self, argv):
        argv = list(reversed(argv))
        res = {}
        for k, v in self.schema.iteritems():
            if v is bool:
                res[k] = False
        
        while argv:
            arg = argv.pop()
            arg = arg[1:]
            typ = self.schema[arg]
            if (typ is bool):
                res[arg] = True
            else:
                res[arg] = typ(argv.pop())
        
        if len(res) != len(self.schema):
            raise KeyError
            
        return res    
        
        
doctest.testmod()