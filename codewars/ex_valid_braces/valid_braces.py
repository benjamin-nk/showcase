# https://www.codewars.com/kata/5277c8a221e209d3f6000b56

def valid_braces(string):
    stack = []
    cbrace_map = {
        '}': '{',
        ')': '(',
        ']': '[',
    }
    for c in string:
        if c not in ['(',')','{','}','[',']']: continue
        
        peek = len(stack) > 0 and stack[len(stack)-1] or None
        
        # completed brace check
        if c in [')','}',']']:
            # check top item for opening brace, if not present then return false else 
            if peek != cbrace_map[c]:
                return False
            else:
                stack.pop()
            
        # append opening brackets
        else:
            stack.append(c)
        
    return len(stack) == 0