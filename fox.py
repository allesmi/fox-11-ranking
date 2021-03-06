#!/usr/bin/env python3

import urllib.request
import csv
import sys

# Published Google Spreadsheet:
url = 'https://docs.google.com/spreadsheets/d/1qDaw9-JDPdo7Fq-NEXQS55dSnSrxGJOTYqbYvDBwOV4/pub?gid=0&single=true&output=csv'
# Cycle,Winner,ENL Score,RES Score,#1,#2,#3

def log(msg):
	print(msg, file=sys.stderr)

# Get file and store locally
log('Downloading data file ...')
datafile = 'data.csv'
try:
	response = urllib.request.urlretrieve(url, datafile)
except Exception:
	log("Error downloading file")
	sys.exit(-1)

# Closure to count points
def add_rank(scores, score):
	def add_n_rank(name):
		if not name:
			return

		if name not in scores:
			scores[name] = 0

		scores[name] = scores[name] + score

	return add_n_rank

scores = {}
top_3_points = [
	add_rank(scores, 100),
	add_rank(scores, 80),
	add_rank(scores, 60)
	]

faction_scores = {}
faction_top_10_points = [
	add_rank(faction_scores, 100),
	add_rank(faction_scores, 80),
	add_rank(faction_scores, 60),
	add_rank(faction_scores, 50),
	add_rank(faction_scores, 45),
	add_rank(faction_scores, 40),
	add_rank(faction_scores, 36),
	add_rank(faction_scores, 32),
	add_rank(faction_scores, 28),
	add_rank(faction_scores, 26)
	]

log('Counting scores ...')

enl_score = 0
res_score = 0
with open(datafile) as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		cycle = row[0]
		winner = row[1].lower()
		enl = row[2]
		res = row[3]
		top_3 = row[4:7]
		faction_top_10 = row[7:]

		if cycle in ["avg", "Cycle"]:
			continue

		if winner == "enl":
			enl_score += 1
		elif winner == "res":
			res_score += 1

		for rank, agent in enumerate(top_3):
			top_3_points[rank](agent)

		for rank, agent in enumerate(faction_top_10):
			faction_top_10_points[rank](agent)


def print_ranking(scores):
	rank = 0
	prev = 0
	print("# RANK\tAGENT\tPOINTS")
	for (agent, points) in reversed(sorted(scores.items(), key=lambda x: x[1])):
		if prev is not points:
			rank += 1
			prev = points
		print("{}\t{}\t{}".format(rank, agent, points))

print("RES {} : {} ENL".format(res_score, enl_score))
print_ranking(scores)
print_ranking(faction_scores)