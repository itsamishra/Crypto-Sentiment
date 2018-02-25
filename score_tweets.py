#!/usr/bin/python3

import sentiment_mod as s
import csv

# 
def screen_tweets(text):
	if text[0]=="@":
		return False
	blacklisted_phrases = ["rt ", "eth", "ethereum", "bitcoin cash", "bcash", "ltc", "litecoin"]

	for phrase in blacklisted_phrases:
		if phrase in text:
			return False

	return True


tweets = []
with open("tweets.tsv", "r", newline="") as fp:
	read_tsv = csv.reader(fp, delimiter="\t")

	for i in read_tsv:
		if i[12]!="text":
			tweets.append(i[12])

# TODO replace current TSV solution with Google Sheets "database" solution (see: https://www.youtube.com/watch?v=vISRn5qFrkM)
# TODO find a way of getting all text from tweets (no "..." at end of text)

for i in tweets:
	i_lower = i.lower()
	if screen_tweets(i_lower):
		sentiment = s.sentiment(i)
		if sentiment[1]==1:
			print(i)
			print(s.sentiment(i))
			print("=========================================")