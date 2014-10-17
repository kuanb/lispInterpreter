import compiler

# contentReadInit = '(+ (+ (* 23 4) 99) (- 90 (/ 444 23)))'
contentReadInit = '((lambda (x) x)'

varDictionary = {}

def readContentIn(contentRead):

	contentRead = contentRead.replace('(', ' ( ')
	contentRead = contentRead.replace(')', ' ) ')
	contentRead = contentRead.split(' ')
	contentRead = filter(lambda a: a != '', contentRead)
	return contentRead

def checkType(char):
	try:
		return {'type': 'numeric', 'value': float(char)}
	except ValueError:
		if char[0] is "'" and char[-1] is "'":
			return {'type': 'strVal', 'value': str(char[1:-1])}
		else:
			return {'type': 'identifier', 'value': str(char)}

# method that is trying to avoid the global variable from peter norvig's solution
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
		raise SyntaxError('Code has a hanging end paranthesis.')
	else:
		return checkType(firstChar), content

def evaluate(listInput):
	# base case
	if not type(listInput) is list:
		return listInput
	
	# operations
	operator = listInput[0]
	if not type(operator) is list and operator in '+/-*':
		result = eval(str(evaluate(listInput[1])) + operator + str(evaluate(listInput[2])))
		return result
	if operator is 'lambda':
		print 'hello'
		return None

	# control for 'double nested' lists that happen with lambda and define, etc.
	elif type(operator) is list:
		 f = evaluate(operator)




def wrapperRun(contentInput):
	read = readContentIn(contentInput)
	parsedList, _ = parseContent('', read)
	return parsedList



print wrapperRun(contentReadInit)
