## Roman Numerals Kata
##
## See http://commentsarelies.blogspot.com/2008/09/roman-numerals.html
## Written by Johan Lindberg

def as_roman_numeral(num):
    """
    Returns a string containing the roman numeral representation of num or
    None if num is outside of range(1,4000).
    
    >>> as_roman_numeral(4000) == None
    True
    >>> as_roman_numeral(1)
    'I'
    >>> as_roman_numeral(99)
    'XCIX'
    >>> as_roman_numeral(888)
    'DCCCLXXXVIII'
    >>> as_roman_numeral(1999)
    'MCMXCIX'
    >>> as_roman_numeral(2001)
    'MMI'
    """
    
    units       = [0, 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX']
    tens        = [0, 'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC']
    hundreds    = [0, 'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM']
    thousands   = [0, 'M', 'MM', 'MMM']
    
    if num in xrange(1,4000):
        th, mils = num//1000, num%1000
        h, cents = mils//100, mils%100
        te, u    = cents//10, cents%10
        return "".join(numerals[digit] for digit, numerals in [(th, thousands),
                                                               (h, hundreds),
                                                               (te, tens),
                                                               (u, units)] if digit > 0)
    else:
        return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    import sys
    print as_roman_numeral(int(sys.argv[-1]))
