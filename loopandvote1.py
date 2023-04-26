import csv
import infinite_vote

def loopthis(csv1,start_range=1,end_range=2):
	voted = 0
	with open(csv1,newline='') as csvfile:
		datareader = list(csv.reader(csvfile, delimiter=',', quotechar='|'))
		if end_range == 2:
			end_range = len(datareader)
		for i in range(start_range,end_range):
			print(datareader[i][0])
			print(datareader[i][1])
			infinite_vote.vote(datareader[i][0],datareader[i][1])
			voted += 1
			print('accounts gone thru by loopandvote1: '+ str(voted))

