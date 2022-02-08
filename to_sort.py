ls = [1, 2, 3, 0, 4, 6, 5, 7, 8, 10, 9, 13, 12, 14, 11, 15, 17, 18, 19, 16, 20, 22, 21, 23, 24, 25, 31, 26, 27, 28, 29, 30]

def find_swaps(ls):
	i=0
	total_swaps = 0
	while i < len(ls):
		temp = ls[i]
		while i != ls[i]:
			print("index {} swaps with {}".format(i, ls[i]))
			total_swaps +=1
			ls[i],ls[temp] = ls[temp],ls[i]
			temp = ls[i]
		i+=1
	print(total_swaps)
