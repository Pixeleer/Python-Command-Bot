'''
    PROGRAM: PEMDAS ALGORITHM O(1)
    DATA: 12/29/21
    ORDER:
        Parentheses
        Exponent
        MULTIPLICATION
        DIVISION
        ADDITION
        SUBTRACTION
'''


# Take in input (already in context)
# Group all parenthesed context



# def = define (function)


def GROUP(context):
    equation_queue = list()
    stack = list()
    for i in range(len(context)):
        if context[i] == '(':
            stack.append(i)
        elif context[i] == ')':
            if len(stack) != 0:
                # HEY WE FOUND MATCHING OPENING AND CLOSING
                at = stack.pop()+1
                equation_queue.append( context[at : i])

    if equation_queue != []:
        if equation_queue[-1] != context:
            equation_queue.append(context)
        elif equation_queue[-1] != context[1:-1]:
            equation_queue.append(context[1:-1])

    return equation_queue if equation_queue != [] else [context]




def FIT(original, subs):
    if subs == [] or original == []:
        return original

    new = list()
    opened = 0

    stack = list()
    for i in range(len(original)):
        if original[i] == '(':
            stack.append(i)
            opened += 1
        elif original[i] == ')':
            if len(stack) != 0:
                new.append(subs.pop())
                stack.pop()

            opened -= 1
        elif opened == 0:
            new.append(original[i])

    return new if new != original else subs

def PEMDAS(eq=None):
    eq = eq or []

    operators = []
    operands = []

    # Challenge O(n) tike complexity
    ops = ('^', '*', '/', '+', '-')


    def calc(a, op,b):
        if op == '+':
            return a+b
        
        if op == '-':
            return a-b
            
        if op == '*':
            return a*b

        if op == '^':
            return a**b
        
        if op == '/':
            return a/b


    info = list() # list of ops and their indexes
    for i in range(len(eq)):
        _ = eq[i]
        if _ in ops:
            info.append((_, i))

    length = len(info)
    info.sort(
        key=lambda I: ops.index(I[0]) if I[0] not in ['+','-'] else length
    )

    operands = list(map(
        lambda _: [    _[1]-1   ,     _[1]+1    ], # get a and b from arr
        info
    ))

    operators = list(map(lambda _: _[0],info))


    ''' IDEA
    create a placeholder list that repr the place for the awaiting result to go
    '''

    res = None
    x = None

    results = list()
    used = list()

    for _ in operands:
        a,b = _

        a = results.pop() if results != [] and a in used else eq[a]
        b = results.pop() if results != [] and b in used else eq[b]
        used += _

        op = operators.pop(0)
    
        res = calc(int(a), op,int(b))
        results.append(res)
   
    return res


def dotheting(group):
    results = list()

    for i in range(len(group)):
        # each group is a piece of the next
        # get the index of the first ch in current group
        # use that index as a position for the res in the next group
        context = group[i]
        res = PEMDAS(context)
        if i+1 < len(group):
            results.append(res)
            rev = list(reversed(results))
            fitting = FIT(group[i+1], rev)
            group[i+1] = fitting
            

        else:
            return res or results[-1]



def getEquations(context, math_keywords=list(), variables=dict()): # <LIST>, <DICTIONARY>
    new = list()

    hasOP = False
    
    ops = ('(',')','^', '*', '/', '+', '-')

    eq = list()

    for i in range(len(context)):
        ch = context[i]
        if not (ch.isdigit() or ch in ops or ch in math_keywords or ch in variables.keys()):
            # Not an operand or operator
            # check if eq was built
            hasOP = sum([_ in ops for _ in eq]) != 0 # check if eq has op characters
            if eq != [] and hasOP:
                new.insert(len(new),eq)

            elif eq != []:
                new += eq   # add accidental characters

            eq = list()
            hasOP = False

            new.append(ch)
            # append this ch to new context
        else:
            ch = variables.get(ch,ch)
            # append eq ch to eq
            eq.append(ch)


    hasOP = sum([_ in ops for _ in eq]) != 0 # check if left over eq has op characters
    if hasOP:
        new.insert(len(new),eq)
    else:
        new += eq



    return new

