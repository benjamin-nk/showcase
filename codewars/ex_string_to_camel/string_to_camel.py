# https://www.codewars.com/kata/517abf86da9663f1d2000003

def to_camel_case(text):
    if text == '': return ''

    stack = []
    s = ''
    for c in text:
        
        if len(stack) != 0: 
            peek = stack[len(stack)-1] 
        else:
            peek = None
                    
        # if the last character was a hyphen or underscore than make the current char uppercase
        if peek is not None and peek in ['-','_']:
            s = s + c.upper()
        # do not add hyphens or underscores to new string
        elif c not in ['-','_']:
            s = s + c
        stack.append(c)
            
    return s