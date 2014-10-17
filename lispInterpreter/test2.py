import compiler

contentReadInit = '(+ (* 2 9) (- 8 2)))'
#contentReadInit = '((lambda (x) x)'

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
	contextHolder = {}

def wrapperRun(contentInput):
	read = readContentIn(contentInput)
	parsedList, _ = parseContent('', read)
	return parsedList

def checkUndefined(toTest):
	try:
		toTest
	except NameError:
		return True
	else:
		return False

class scopeController:
	def __init__(self, scope, parent):
		self.scope = scope
		self.parent = parent
	def get(identifier):
		if identifier in self.scope:
			return self.scope[identifier]
		elif checkUndefined(self.parent) is True:
			return self.parent.get(identifier)

def interpret(input, context):
	if context is True:
		return interpret(input, new scopeController(library))



print wrapperRun(contentReadInit)
