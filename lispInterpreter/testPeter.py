from math import pi
from copy import copy

### Lisp Interpreter

# basic functions called on
def is_self_evaluating(inputVal):
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

# basic arithmetic
def lisp_minus(args): pass
def lisp_mult(args): pass

def lisp_abs(args):
    assert_arguments("abs", len(args) == 1)
    return abs(args[0])

globalEnv = {
	"+": lambda args: sum(args),
    "-": lisp_minus,
    "*": lisp_mult,
    "abs": lisp_abs,
    "car": lambda args: return args[0],
    "cdr": lambda args: return args[1:],
    "pi": pi
}

# begins tasks to parse and eval content
def repl():
    while True:
        print_prompt()
        lisp_print(lisp_eval(lisp_read(line), globalEnv))

# parse and re-interpret content
def lisp_read(input):
	pass

# evaluate parsed content
def lisp_eval(sexp, env):
    if type(sexp) is list:
        return lisp_eval_list(sexp, env)
    else:
        return lisp_eval_atom(sexp, env)

# atoms
def lisp_eval_atom(sexp, env):
    if is_self_evaluating(sexp):
        return sexp
    else is_symbol(sexp):
        if sexp in env:
            return env[sexp]
        else:
            print "No binding for " + sexp
            return None

# lists
def lisp_eval_list(sexp, env):

    head = sexp[0]
    
    # check if it is a unique operation, such as begin
    if is_special_operator(head):
        return lisp_eval_special(sexp, env)
    else:
        # Basic evaluation rule for list
        evaluated = [ lisp_eval(exp, env) for exp in sexp ]
        fn = evaluated[0]
        args = evaluated[1:]
        apply(fn, args, env)

def lisp_eval_special(sexp, env):

    head = sexp[0]
    body = sexp[1:]

    if head == "if":
        cond, yes, no = body
        if lisp_boolean(lisp_eval(cond, env)):
            return lisp_eval(yes, env)
        else:
            return lisp_eval(no, env)

    if head == "quote":
        return body[0]

    if head == "define":
        name, value = body
        if is_symbol(name): # is a Python string
            env[name] = value
        elif type(name) is list:
            fn = name[0]
            args = name[1:]
            env[fn] = ["lambda", args, value]
        return value

    if head == "begin": pass

    if head == "lambda":
        variables, body = sexp[1:]
        new_env = ...
        return lambda *args: 

        return sexp

def apply(fn, args, env):
    if is_lambda(fn):
        variables, body = fn[1:]
        new_env = copy(env)

        assert_arguments(fn, len(args) == len(variables))

        for (variable, value) in zip(variables, args):
            new_env[variables] = value
            # body = ["+", "x", "10"]
        return lisp_eval(body, new_env)
    else:
        # fn is primitive function
        return globalEnv[fn](args)

def lisp_boolean(x):
    if x == "#t":
        return True
    elif x == "#f":
        return False
    else:
        fail("Not a boolean.")



