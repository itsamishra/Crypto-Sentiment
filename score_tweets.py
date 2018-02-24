#!/usr/bin/python3

import sentiment_mod as s
import csv

tweets = []
with open("tweets.tsv", "r", newline="") as fp:
	read_tsv = csv.reader(fp, delimiter="\t")

	for i in read_tsv:
		if i[12]!="text":
			tweets.append(i[12])

#TODO remove repetitions from tweets
#TODO find a way of getting all text from tweets (no "..." at end of text)

for i in tweets:
	i_lower = i.lower()
	if "eth" not in i_lower and "cash" not in i_lower:
		sentiment = s.sentiment(i)
		if sentiment[1]==1:
			print(i)
			print(s.sentiment(i))
			print("=========================================")