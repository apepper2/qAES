def rcon(n):
	rconstants = [
	[0, 0, 0, 0, 0, 0, 0, 1],
	[0, 0, 0, 0, 0, 0, 1, 0],
	[0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 0],
	[0, 0, 0, 1, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 0, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0],
	[1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 1, 1, 0, 1, 1],
	[0, 0, 1, 1, 0, 1, 1, 0]
	]
	return(rconstants[n+1])



def bitwise_CNOT(control, target): #assuming same dimensions
	rv = []
	for i in range(control):
		control_bit = control[i]
		target_bit = target[i]
		rv += ["CNOT({},{})".format(control[i],target[i])]
	return(rv)

def write_const(constant, target):
	rv = []
	for idx,val in enumerate(constant):
		if val == 1:
			rv += ["X({})".format(target[idx])]
	return(rv)


def key_schedule(key, W): #word slots has capacity for 8 words, 256 qubits
	key_as_words = [key[i:i+32] for i in range(0,len(key),32)] #4 words

	for i in range(4):
		yield write_const(key_as_words[i],W[i])
	s=4
	t=43
	cur_slot = 4


	for i in range(s,t):
		if cur_slot < 8:
			if 0 == i%s:
				if i == 4:
					rv = bitwise_CNOT(W[0],W[4])
					rv+= bitwise_CNOT(Subword(RotWord(W[3])), W[4])
					rv+= write_const(rcon(1))
					yield rv
					
				elif i == 8:	
					rv = bitwise_CNOT(W[cur_slot-s],W[cur_slot])
					rv += bitwise_CNOT(SubWord(RotWord(W[cur_slot-1])), W[cur_slot]) 
					rv += write_const(rcon(i/s))
					yield rv
			else:
				rv = bitwise_CNOT(W[cur_slot-(s-(i%s))], W[cur_slot])
				yield rv
				if 3==i%s:
					cur_slot+=1
		else:
			slot = 4
			if 0 == i%s:
				rv = bitwise_CNOT(W[slot-s],W[cur_slot])
				rv += bitwise_CNOT(SubWord(RotWord(W[cur_slot-1])), W[cur_slot]) 
				rv += write_const(rcon(i/s))
				yield rv
			else:
				rv = bitwise_CNOT(W[cur_slot-(s-(i%s))], W[cur_slot])
				yield rv
				if 3==i%s:
					cur_slot+=1