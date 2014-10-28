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
    return abs(args)

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

def is_special_operator(inputVal):
    if not inputVal in globalEnv:
        return True
    else:
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
            print "No binding for " + sexp
            return None
    else:
        print "No idea what this atom is: " + sexp
        return None

# lists
def lisp_eval_list(sexp, env):
    operator = sexp[0]

    if is_special_operator(operator):
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

    # if operator == "define":
    #     name, value = body
    #     if is_symbol(name): # is a Python string
    #         env[name] = value
    #     elif type(name) is list:
    #         fn = name[0]
    #         args = name[1:]
    #         env[fn] = ["lambda", args, value]
    #     return value

    # if operator == "begin": pass

    # if operator == "lambda":
    #     variables, body = sexp[1:]
    #     new_env = ...
    #     return lambda *args: 

    #     return sexp

def evalApply(fn, args, env):
    try:
        fn[0]
        if fn[0] == 'lambda':
            variables, body = fn[1:]
            new_env = copy(env)
            assert(fn and len(args) == len(variables))
            for (variable, value) in zip(variables, args):
                new_env[variables] = value
            return lisp_eval(body, new_env)
    except TypeError:
        # fn is primitive function
        return fn(args)


contentReadInit = "(if (= 1 1) (+ 2 3) (+ 0 0))"


def wrapperRun(contentInput):
    print 'Lisp input is:', contentInput
    read = readContentIn(contentInput)
    parsedList, _ = parseContent('', read)
    print 'Parsed list is:', parsedList
    return str('Final output: ' + str(lisp_eval(parsedList, globalEnv)))

print wrapperRun(contentReadInit)
