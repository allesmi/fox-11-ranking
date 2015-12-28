#!/usr/bin/env python3

import urllib.request
import csv

# Published Google Spreadsheet:
url = 'https://docs.google.com/spreadsheets/d/1qDaw9-JDPdo7Fq-NEXQS55dSnSrxGJOTYqbYvDBwOV4/pub?gid=0&single=true&output=csv'
# Cycle,Winner,ENL Score,RES Score,#1,#2,#3

# Get file and store locally
print('Downloading data file ...')
datafile = 'data.csv'
response = urllib.request.urlretrieve(url, datafile)

# Closure to count points
def add_rank(score):
	def add_n_rank(name):
		if not name:
			return

		if name not in scores:
			scores[name] = 0

		scores[name] = scores[name] + score

	return add_n_rank

add_first_rank = add_rank(100)
add_second_rank = add_rank(80)
add_third_rank = add_rank(60)

print('Counting scores ...')
scores = {}
with open(datafile) as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		cycle = row[0]
		winner = row[1]
		enl = row[2]
		res = row[3]
		first = row[4]
		second = row[5]
		third = row[6]

		if cycle in ["avg", "Cycle"]:
			continue

		add_first_rank(first)
		add_second_rank(second)
		add_third_rank(third)

rank = 0
prev = 0
print("RANK\tAGENT\tPOINTS")
for (agent, points) in reversed(sorted(scores.items(), key=lambda x: x[1])):
	if prev is not points:
		rank += 1
		prev = points
	print("{}\t{}\t{}".format(rank, agent, points))
