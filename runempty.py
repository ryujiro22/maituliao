import csv
import votingbot

voted = 0

with open('empty.csv',newline='') as csvfile:
	datareader = list(csv.reader(csvfile, delimiter=',', quotechar='|'))

	for i in range(1,len(datareader)):
		print(datareader[i][1])
		print(datareader[i][2])
		votingbot.vote(datareader[i][1],datareader[i][2])
		voted += 1
		print('accounts gone thru by loopempty: '+ str(voted))