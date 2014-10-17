# given holder, hardcoded
holder = "(/ (+ 3  ( * 2 3 )) (- 4 2))"

# holder cleaning
holder = holder.replace( '(' , ' ( ' )
holder = holder.replace( ')', ' ) ' )
holder = holder.split(' ')
holder = filter(lambda a: a != '', holder)

# switch for while loop to parse through the data iteratively
switch = 1

# while loop
while switch == 1:
	
	for place in range(0,len(holder)-1): 
		if  holder[place] == ')':
			# trigger back search for a parans
			a = []				
			
			for position in range(0,place-1):
				# finding the points where there are open parans
				if holder[position] == '(':
					a.append(position)
				else: 
					pass
			# get the most recent parans
			biggest = max(a)

			# calculate subParans equation, return var part
			opp = holder[biggest+1]
			num1 = holder[biggest+2]
			num2= holder[biggest+3]
			part = eval(num1 + opp + num2)
			part = str(part)
			
			temp = holder[:biggest] 
			try:
  mylist[i] += 1
except IndexError:
  print "No item at ", i
			temp = temp + holder[biggest+5:]

			holder = temp
			print temp, "xx"
			break
			
	if not '(' in holder: 
		switch = 0 
		print "done"