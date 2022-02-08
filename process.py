with open('mix_columns_raw.txt') as f:
	for line in f.readlines():
		lhs,rhs = line.strip().replace(" ", "").split("=")
		lhs = lhs[0] + "[" + lhs[1:] + "]"
		for i in rhs.split("^"):
			i = i[0] + "[" + i[1:] + "]"
			print("CNOT({},{})".format(i,lhs))