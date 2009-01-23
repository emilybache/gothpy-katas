Flags in the schema are specified as keyword parameter arguments to the
function make_parser. The key is the name of the flag and the value is a
function call to flag which contains information about the expected type
and an optional default value.

>>> from kataargs import *
>>> parse = make_parser(a = flag(int, default = 0))
                                  
The example above constructs a parser for a schema with one flag (a) which
can have exactly one int value associated with it. If no value is given it
will default to 0.

>>> values = parse(['-a', '42'])
>>> print(values['a'])
42
>>> values = parse([])
>>> print(values['a'])
0


The parser is reusable so we only call make_parser once for each schema we
wish to parse. Trying to parse an unspecified flag, or associating a flag
with something other than its expected type will result in an Exception.

>>> values = parse(['-b', '42'])
Traceback (most recent call last):
    ...
Exception: No flag named 'b' have been specified for this parser.

>>> values = parse(['-a', 'foo'])
Traceback (most recent call last):
    ...
Exception: Expected value of type: <class 'int'> for flag: a.


Arguments can be parsed in any order. If a flag appears twice in the
arguments, the last value is returned.

>>> parse = make_parser(a = flag(int, default = 0),
...                     b = flag(int, default = 1),
...                     c = flag(int, default = 2))
>>> values = parse(['-c', '2', '-a', '1', '-b', '0', '-a', '3'])
>>> print(values['a'])
3


If you specify an expected type of None for a flag, it will be associated
with the value True if it is present in the list of arguments. If it is
not present, it will be given the value False regardless of which default
value was specified.

>>> parse = make_parser(a = flag(None, default = False),
...                     b = flag(None))

>>> values = parse(['-a', '-b'])
>>> print(values['a'])
True
>>> print(values['b'])
True

>>> values = parse([])
>>> print(values['a'])
False
>>> print(values['b'])
False

If you specify an arity of N (many) for a flag, it will be associated with
a list of values (of the expected type). It will always default to the
empty list, regardless of what you specify.

>>> parse = make_parser(a = flag([int], default = None))
>>> values = parse(['-a', '4', '2'])
>>> print(values['a'])
[4, 2]

>>> values = parse([])
>>> print(values['a'])
[]


An Exception is thrown if an argument cannot be associated with a flag

>>> parse = make_parser(a = flag(None, default = False))
>>> values = parse(['-a', '1'])
Traceback (most recent call last):
    ...
Exception: No flag can be associated with value: 1.

>>> values = parse(['1','-a', '2'])
Traceback (most recent call last):
    ...
Exception: No flag can be associated with value: 1.


If a flag has arity 1 but is passed several arguments it is associated with
the last of them.

>>> parse = make_parser(a = flag(int))
>>> values = parse(['-a', '1', '2', '3'])
>>> print(values['a'])
3


If a flag has arity 0 but is passed one or more arguments, an Exception is
thrown.

>>> parse = make_parser(a = flag(None))
>>> values = parse(['-a', '1', '2', '3'])
Traceback (most recent call last):
    ...
Exception: No flag can be associated with value: 1.


You must specify an expected type when calling make_parser.

>>> parse = make_parser(a = flag())
Traceback (most recent call last):
    ...
TypeError: flag() takes at least 1 positional argument (0 given)


Schemas are validated before a parser is created for handling it. The
validation rule is quite simple.

1) Expected type must be a built-in type like str, float, int or bool.

>>> def foo(v): return v
>>> parse = make_parser(a = flag(foo))
Traceback (most recent call last):
    ...
Exception: Schema validation failure: Expected type must be a built-in type.
