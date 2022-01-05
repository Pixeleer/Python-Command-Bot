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

def numify(num):
    try:
        return float(num)
    except:
        return num

def isNum(num):
    return isinstance(numify(num), (int,float))

def PEMDAS(eq=[]):
    if len(eq) == 1:
        return eq[0]
    elif len(eq) < 3:
        return 'err'

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

        a,b = numify(a),numify(b)
        if not (isNum(a) and isNum(b)):
            return 'err'

        used += _

        op = operators.pop(0)
    
        res = calc(a, op,b)
        results.append(res)
   
    return res


def solve(group):
    results = list()

    for i in range(len(group)):
        # each group is a piece of the next
        # get the index of the first ch in current group
        # use that index as a position for the res in the next group
        context = group[i]
        res = PEMDAS(context)
        if res == 'err':
            return None

        if i+1 < len(group):
            results.append(res)
            rev = list(reversed(results))
            fitting = FIT(group[i+1], rev)
            group[i+1] = fitting
            

        else:
            return res or (results[-1] if results != [] else None)



def getEquations(context, math_keywords=list(), variables=dict(), ignore=list()): # <LIST>, <DICTIONARY>, <LIST>
    new = list()
    
    ops = ('=','(',')','^', '*', '/', '+', '-')
    signed = False
    eq = list()

    def checkEq():
        hasOp = sum([_ in ops for _ in eq]) != 0
        ofLength = len(eq) >= 3
        return hasOp and ofLength

    assignment = ['=','equals','is equal to']

    for i in range(len(context)):
        left = context[i-1] if i > 0 else None
        right = context[i+1] if i+1 < len(context) else None
        ch = context[i]
        var = False     # acts as variable?
        if i+1 < len(context) and context[i+1] in assignment:
            var = True
        else:
            var = False
            ch = ch if left in ignore and (right not in ops and not isNum(right))  else variables.get(ch,ch)
            ch = str(ch)

        if signed and ch.isdigit():
            eq[-1] += ch
            continue


        if not (isNum(ch) or ch in ops or ch in math_keywords or ch in variables.keys() or var) or ch in ignore:
            # Not an operand or operator
            # check if eq was built
            if checkEq():
                new.insert(len(new),eq)
            elif eq != []:
                new += eq   # add accidental characters

            eq = list()

            new.append(ch)
            signed = False
            # append this ch to new context
        else:

            '''First solution for shorthand '''
            pre = variables.get(left,')' if left == ')' else None)
            post = variables.get(right,'(' if right == '(' else None)

            # if pre ch is ')' or numeric | if post ch is '(' or numeric
            pre,post = pre == ')' or isNum(pre), post == '(' or isNum(post)

            if pre and (eq != [] and eq[-1] != '*') and ch not in ops:  # shorthand * with what comes before ch
                eq.append('*')
 
            eq.append(ch)

            if post and ch not in ops:  # shorthand * with what comes after ch
                eq.append('*')

            signed = False

            if eq[0] in ('+','-') and not (i > 0 and left.isdigit()):   # Signed number
                signed = True

    check = checkEq()
    if check and eq[0] in ops and not signed:    # signed number
        new += [''.join(eq)]
        
    elif check:        
        new.insert(len(new),eq)
    else:
        new += eq

    return new
