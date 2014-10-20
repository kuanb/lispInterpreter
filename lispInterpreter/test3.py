import compiler

# operations completed: arithmetic, lambda
#contentReadInit = '(+ (- ((lambda (a) (* 2 a)) 2) 3) 2)'
#contentReadInit = '((lambda (x) (+ x 3)) 2)'
#contentReadInit =  '(+ ((define (add1 x) (+ 1 x)) (add1 3)) ((lambda (x) (+ x 3)) (abs -4)))'
#contentReadInit = '(list 1 2 (+ 7 2) 4)'
#contentReadInit = '(if (not (= 1 1)) 1 0)'
#contentReadInit = "(cond ((> 3 4) 'greater) ((< 3 1) 'less) ((< 3 2) 'mea) ((> 3 12) 'lests) (else (+ 1 1)))"
contentReadInit = '(else (+ 1 1))'


varDictionary = {}

def readContentIn(contentRead):

	contentRead = contentRead.replace('(', ' ( ')
	contentRead = contentRead.replace(')', ' ) ')
	contentRead = contentRead.split(' ')
	contentRead = filter(lambda a: a != '', contentRead)
	return contentRead

def checkType(char):
	try:
		return float(char)
	except ValueError:
		return str(char)

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

def checkUndefined(toTest):
	try:
		toTest
	except NameError:
		return True
	else:
		return False

def evaluate(listInput, stateDict):
	# base case
	if not type(listInput) is list:
		try:
			return stateDict[listInput]
		except KeyError:
			try:
				return float(listInput)
			except ValueError:
				if listInput[0] == '"' or listInput[0] == "'":
					return listInput[1:]
				else:
					return listInput

	# operations subsection
	operator = listInput[0]

	# operations on lists
	if type(operator) is list:

		# handle lambdas and convert them into results
		if operator[0] == 'lambda':
			lambdaDict = {}
			lambdaDictCounter = 0
			for i in operator[1]:
				lambdaDict[i] = listInput[lambdaDictCounter+1]
				lambdaDictCounter += 1
			toRedefine = operator[2]

			# works through and replaces all variables within lambda
			def replaceVars(toRedefine, lambdaDict):
				if type(toRedefine) is list:
					for i in range(len(toRedefine)):
						if type(toRedefine[i]) is list:
							toRedefine[i] = replaceVars(toRedefine[i], lambdaDict)
						elif toRedefine[i] in lambdaDict:
							toRedefine[i] = lambdaDict[toRedefine[i]]
				else:
					toRedefine = lambdaDict[toRedefine]
				return toRedefine
			return evaluate(replaceVars(toRedefine, lambdaDict), stateDict)

		# handle define values
		elif operator[0] == 'define':
			if type(operator[1]) is list:
				forDict = ['lambda']
				# create the sublist of variables
				forDictVars = []
				for i in range(1, len(operator[1])):
					forDictVars.append(operator[1][i])
				forDict.append(forDictVars)
				# create the sublist of the substitute equation
				forDict.append(operator[2])
				stateDict[operator[1][0]] = [forDict]
				return evaluate(listInput[1:], stateDict)
			elif type(operator[1]) is str:
				stateDict[operator[1]] = evaluate(operator[2], stateDict)
				return evaluate(listInput[1:], stateDict)

		elif operator[0] == 'list':
			buildList = []
			for i in range(1, len(operator)):
				buildList.append(i)
			return buildList

		# just recurse on the first item of listInput and return that, to work down nested lists
		else:
			return evaluate(operator, stateDict)

	# basic string operations
	elif type(operator) is str:
		if operator in '+/-*<=>=':
			if operator == '=':
				operator += operator
			return eval(str(evaluate((listInput[1]), stateDict)) + operator + str(evaluate((listInput[2]), stateDict)))
		elif operator == 'abs':
			return abs(float(evaluate(listInput[1], stateDict)))
		# recurse if nested single variable in a list
		elif operator in stateDict:
			return evaluate(stateDict[operator] + listInput[1:], stateDict)
		# controlling for not
		elif operator == 'not':
			if evaluate(str(listInput[1]), stateDict) is True:
				return False
			else:
				return True
		elif operator == 'if':
			if evaluate(str(listInput[1]), stateDict) is True:
				return evaluate(str(listInput[2]), stateDict)
			else:
				return evaluate(str(listInput[3]), stateDict)
		elif operator == 'else':
			return evaluate(listInput[1], stateDict)
		elif operator == 'cond':
			for i in listInput[1:]:
				if evaluate(str(i), stateDict) is True:
					return evaluate(str(i[1]), stateDict)
				elif i[0] == 'else':
					return evaluate(i[1], stateDict)

	# to catch just in case there are any floats that slip through
	elif type(operator) is float:
		return operator

	# for programming review purposes
	print "WARNING! Failed parse.\nLast catch:", listInput, "\nWith current dictionary:", stateDict

def wrapperRun(contentInput):
	print 'Lisp input is:', contentInput
	read = ['('] + readContentIn(contentInput) + [')']
	parsedList, _ = parseContent('', read)
	print 'Parsed list is:', parsedList
	return str('The answer is: ' + str(evaluate(parsedList, {})))

print wrapperRun(contentReadInit)
