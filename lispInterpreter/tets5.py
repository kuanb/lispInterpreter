from math import pi
from copy import copy



### Read in content, spread it out and create single list

def readContentIn(contentRead):

    contentRead = contentRead.replace('(', ' ( ')
    # contentRead = contentRead.replace('[', ' ( ')
    contentRead = contentRead.replace(')', ' ) ')
    # contentRead = contentRead.replace(']', ' ) ')
    contentRead = filter(lambda a: a != '', contentRead.split(' '))
    return contentRead



### Parse content and move into nested lists

def parseContent(currentParsedInput, contentInput):
    content = contentInput
    if len(content) == 0:
        raise SyntaxError('Lisp program ended unexpectedly - incomplete code.')
    firstChar = content[0]
    content = content[1:]
    if firstChar == '(':
        tempList = []
        while content[0] != ')':
            toAppend, contentRev = parseContent('', content)
            tempList.append(toAppend)
            content = contentRev
        content = content[1:] # pops off the last '('
        return tempList, content
    elif firstChar == ')':
        raise SyntaxError('EOF Error')
    else:
        return testFloatElseString(firstChar), content



### Depth clean

def depthClean(inputList):
    if type(inputList) is list:
        while len(inputList) == 1 and type(inputList) is list:
            inputList = inputList[0]
    for i in range(len(inputList)):
        if not type(inputList[i]) is list:
            pass
        else:
            inputList[i] = depthClean(inputList[i])
    return inputList



### Global environment

def geAdd(args):
    return sum(args)

def geSubtract(args):
    return reduce(lambda x, y: x-y, args)

def geMultiply(args):
    return reduce(lambda x, y: x*y, args)

def geDivide(args):
    return reduce(lambda x, y: x/y, args)

def geEqual(args):
    return reduce(lambda x, y: x==y, args)

def geAbs(args):
    try:
        assert len(args) == 1
        return abs(args[0])
    except AssertionError:
        print "Cannot take abs() of ", args
        return None

def geCar(args):
    return args[0]

def geCdr(args):
    return args[1:]

globalEnv = {
    "+": geAdd,
    "-": geSubtract,
    "*": geMultiply,
    "/": geDivide,
    "=": geEqual,
    "abs": geAbs,
    "car": geCar,
    "cdr": geCdr,
    "pi": pi
}



### Global functions

def testFloatElseString(char):
    try:
        return float(char)
    except ValueError:
        return str(char)

def is_number(inputVal):
    try:
        int(inputVal)
        return True
    except ValueError:
        try:
            float(inputVal)
            return True
        except ValueError:
            return False

def is_symbol(inputVal):
    try:
        int(inputVal)
        return False
    except ValueError:
        try:
            float(inputVal)
            return False
        except ValueError:
            return True
    except TypeError:
        return False

def lisp_boolean(x):
    if x == True:
        return True
    elif x == False:
        return False
    else:
        print x, "is not a boolean."
        return None



### Lisp interpreter

def lisp_eval(sexp, env):
    if type(sexp) is list:
        return lisp_eval_list(sexp, env)
    else:
        return lisp_eval_atom(sexp, env)

# atoms
def lisp_eval_atom(sexp, env):
    if is_number(sexp):
        return sexp
    elif is_symbol(sexp):
        if sexp in env:
            return env[sexp]
        elif sexp[0] == '"' or sexp[0] == "'":
            return sexp[1:]
        else:
            print "ERROR: No binding for " + sexp
            return None
    else:
        print "No idea what this atom is: " + sexp
        return None

# lists
def lisp_eval_list(sexp, env):
    operator = sexp[0]
    if type(operator) is list and operator[0] == 'lambda':
        return lisp_eval_special(sexp, env)
    elif not operator in env:
        return lisp_eval_special(sexp, env)
    else:
        # Basic evaluation rule for list
        evaluated = [ lisp_eval(exp, env) for exp in sexp ]
        fn = evaluated[0]
        args = evaluated[1:]
        return evalApply(fn, args, env)

def lisp_eval_special(sexp, env):
    operator = sexp[0]
    body = sexp[1:]

    if operator == "if":
        cond, yes, no = body
        if lisp_boolean(lisp_eval(cond, env)):
            return lisp_eval(yes, env)
        elif not lisp_boolean(lisp_eval(cond, env)):
            return lisp_eval(no, env)
        else:
            print "Boolean failed to return T/F; returning None."
            return None

    if operator == "quote":
        return body[0]

    if operator == "define":
        name, value = body
        if is_symbol(name):
            env[name] = lisp_eval(value, env)
        elif type(name) is list:
            fn = name[0]
            args = name[1:]
            env[fn] = ["lambda", args, value]
        return env

    # if operator == "begin": pass
    if operator[0] == "lambda":
        return evalApply(operator, body, env)

    #     return sexp

def evalApply(fn, args, env):
    try:
        fn[0]
        if fn[0] == 'lambda':
            variables, body = fn[1:]
            new_env = copy(env)
            assert(fn and len(variables) == len(args))
            for (variable, value) in zip(variables, args):
                new_env[variable] = value
            return lisp_eval(body, new_env)
    except TypeError:
        # fn is primitive function
        cleanArgs = []
        for i in args:
            cleanArgs.append(lisp_eval(i, env))
        return fn(cleanArgs)


# contentReadInit = "(if (= 1 1) (+ 2 3) (+ 0 0))"
# contentReadInit = "(define (con x y) (+ x y)) (con 3 2)"
# contentReadInit = '(define (add1 x) (+ 1 x)) (+ (add1 3) ((lambda (x) (+ x 3)) (abs -4)))'
# contentReadInit = '(+ 3 ((lambda (x) (+ x 3)) (abs -23)))'
contentReadInit = "(define (con x y) (+ x y)) (con 3 ((lambda (x) (+ x 3)) 3))"


def wrapperRun(contentInput, dictIn):
    print 'Lisp input is:', contentInput
    read = ['('] + readContentIn(contentInput) + [')']
    # read = readContentIn(contentInput)
    parsedList, _ = parseContent('', read)
    print 'Parsed list is:', parsedList
    superGlobal = dictIn
    if len(parsedList) > 1:
        print "Multiple components in Lisp input..."
        for com in parsedList[:-1]:
            print "Processing component: ", com
            newDic = lisp_eval(com, superGlobal)
            superGlobal = dict(superGlobal.items() + newDic.items())
        print "Final assembly with last component: ", parsedList[-1]
        return str('Final output: ' + str(lisp_eval(parsedList[-1], superGlobal)))
    else:
        return str('Final output: ' + str(lisp_eval(parsedList[0], superGlobal)))

print wrapperRun(contentReadInit, globalEnv)
