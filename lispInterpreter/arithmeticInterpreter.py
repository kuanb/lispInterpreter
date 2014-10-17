import compiler

# contentReadInit = '(+ (+ (* 23 4) 99) (- 90 (/ 444 23)))'
contentReadInit = '(define x 34) (+ x 3)'

varDictionary = {}

def interpreter(contentRead):
	if not '(' or not ')' in contentRead:
		print contentRead
		print "var Dict", varDictionary
		return contentRead

	contentRead = contentRead.replace('(', ' ( ')
	contentRead = contentRead.replace(')', ' ) ')
	contentRead = contentRead.split(' ')
	contentRead = filter(lambda a: a != '', contentRead)

	paranHold = []
	for item in contentRead:
		paranHold.append(item)
		if item == ')':
			phRev = paranHold[::-1]
			subParan = []
			for subitem in phRev:
				subParan.append(subitem)
				if subitem == '(':
					break
			subParan = subParan[::-1]
			# check if operation is basic arithmetic
			if subParan[1] in ['+', '-', '*', '/']:
				operator = subParan[1]
				first = subParan[2]
				second = subParan[3]
				if first.isdigit() is True:
					pass
				elif first.isdigit() is False:
					# if first[0] == '-' and first[1:].isdigit is True:
					# 	pass
					# else:
					first = varDictionary[first]
				if second.isdigit is True:
					pass
				elif second.isdigit() is False:
					# if second[0] == '-' and second[1:].isdigit is True:
					# 	pass
					# else:
					second = varDictionary[second]
				compiled = eval(first + operator + second)
			# check if case is a definition
			elif subParan[1] == 'define':
				if subParan[2] == '(':
					print "Can't continue, can't handle function definitions..."
					break
				else:
					varDictionary[subParan[2]] = subParan[3]
					compiled = ''
			# check if operator is part of single item operators (only x-val, no need for y)
			elif subParan[1] in ['abs']:
				operator = subParan[1]
				subject = subParan[2]
				compiled = eval(operator + '(' + subject + ')')
			toSearchFor = ' '.join(subParan)
			toSearchIn = ' '.join(contentRead)
			toSearchIn = toSearchIn.replace(toSearchFor, str(compiled))
			interpreter(toSearchIn)
			break

interpreter(contentReadInit)