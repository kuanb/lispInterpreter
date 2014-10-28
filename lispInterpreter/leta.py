#REMEMBER - MY SPECIAL SECTION DOESN'T ACTUALLY WORK YET! 

#------GlOBAL ARRAYS------

symbol = ['+', '-', '*', '/', '<', '>','<=', '=','>=', 'abs', 'list', 'if', 'cond', 'not',
			'set!', 'begin', 'let', 'define', 'lambda']

special = ['set!', 'begin', 'let', 'define', 'lambda']


# ---- TOKENIZE ------ 
def tokenizer(holder):
	
	holder = holder.replace( '(' , ' [ ' )
	holder = holder.replace( ')', ' ] ' )
	final = filter(lambda a: a != '', holder.split(' '))
	
	return final


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
# ---- PARSER ----- 
def parse(tokens):
	if len(tokens) == 0:
		raise SyntaxError('unexpectedly entered function')
	
	token = tokens[0]
	tokens = tokens[1:]

	if token == '[':
		parsed_input = [] #sets new holder as an array
		
		while tokens[0] != ']':
			to_append, tokens = parse(tokens)
			parsed_input.append(to_append)
		tokens = tokens[1:]							#pops off the ')' part
		
		#we add a condition to check if last return
		if len(tokens) > 0:
			return parsed_input , tokens 				#if not last return, need to return current version of holder
		elif len(tokens) == 0 :
			return parsed_input						#if last return, only want to return new_holder
	elif len(tokens) == 0:
		return check_type(token)			
	else:
		return check_type(token), tokens
	
	
	
# ----- USEFUL GLOBAL FUNCTIONS ----- 
def check_type(x):
	try:
		return float(x)
	except ValueError:
		return str(x)
			
def is_number(x):
	try:
		float(x)
		return True
	except ValueError:
		return False	
	except TypeError:
		return False	




# --- DICTIONARY OF VARIABLES --- 
main_dict = { }


#class Environment(object):
#	def __init__(self, args, values):
#		self.args = args
#		self. values = values
#	
#	def action(self, args, values):
#		zip. 
	
	


# ----- INTERPRETER ------- 
def evaluate(list_input):
	print list_input, 'list_input'
	
	if not type(list_input) is list:
	 	return is_atom(list_input)
	
	elif type(list_input) is list:		
		return is_cons(list_input)
		
		


def is_atom(list_input):
	print list_input, 'atom'
	
	if is_number(list_input):			
		return str(list_input)
	elif list_input[0] == "'":   				
		return list_input[1:]
	elif list_input == 'else': 				
		return False	
	elif list_input in symbol:
		return list_input
	else:
		try:
			return main_dict[list_input]			
		except KeyError: 
			return list_input
		except TypeError:
			return list_input







def is_cons(list_input):
	
	head, rest = list_input[0], list_input[1:]
	
	if head in special:
		return call_special(list_input)
	else:
		return call_regular(list_input)





def call_special(list_input):
	head, rest = list_input[0], list_input[1:]
	
	if head == 'lambda':
		args, exp = rest[0], rest[1]
		return lambda args: evaluate(rest[1], Environment)	
	
	if head == 'cond':
		switch = 1
		while switch == 1:
			for item in rest:
				if item[0]:
					switch = 0
					return item[1]
			break

	
	
	
def call_regular(list_input):
	new_list_input =[]
	
	for term in list_input:
		new_list_input.append(evaluate(term))
	
	list_input = new_list_input

	head, rest = list_input[0], list_input[1:]
	print head, rest, 'head and rest'


	#basic math and boolean operations
	if head in ['+', '-', '*', '/', '<', '>', '<=', '=','>=']:
		if head == '=':
			result = eval(str(rest[0]) + '==' + str(rest[1]))
			return result
		else:
			result = eval(str(rest[0]) + head + str(rest[1]))
			return result
	if head == 'not':
		result = eval(head + ' ' + rest[0])  #without the added space python sees 'notTrue' instead of 'not True'
		return result


	#conditional statements	
	if head == 'if':
		condition = rest[0] 
		consequence = rest[1]
		alt = rest[2]
		if evaluate(condition):
			return eval(str(consequence))
		elif not evaluate(condition):
			return eval(str(alt))


	#absolute value
	if head == 'abs':
		if len(list_input) == 2:
			return abs(rest)
		else:
			raise SyntaxError('abs takes only one operand!')


	#quote
	if head == 'quote':
		if len(list_input) == 2:
			return rest[0]
		else:
			raise SyntaxError('quote only takes one operand')

	#lists
	if head == 'list':
		python_list = []
		list_size = len(list_input)
		i = 1
		while i < len(list_input):
			item = evaluate(list_input[i])
			python_list.append(item)
			i += 1
		return python_list
	
	if callable(head):
		if len(rest) == 1:
			input = rest[0]
			print input, 'input'
			return head(input)
		elif len(rest) == 2:
			input = rest[0], rest[1]
			return head(input)






#input = '(< 10 20)'
#input = '(if (< 10 20) (+ 1 1) (+ 2 2))'
#input = '((lambda (x y) (+ x y)) 1 1)'
#input = '4'
input = '(cond ((< 3 2) 1) ((> 3 2) 2))'

#------ Putting Everything Together ------ 
def interpret(input):
	output = evaluate(parse(tokenizer(input)))
	return output

print interpret(input)