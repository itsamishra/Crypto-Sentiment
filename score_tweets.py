#!/usr/bin/python3

import sentiment_mod as s
import csv
import geotext
import pycountry


# Determines whether tweet should be displayed by checking its content against a blacklist
def screen_tweets(text):
	if text[0]=="@":
		return False

	# Growing list of blacklisted phrases
	blacklisted_phrases = ["rt ", "eth", "ethereum", "bitcoin cash", "bcash", "ltc", "litecoin"]

	# If the text contains any one of the phrases, doesn't display tweet
	for phrase in blacklisted_phrases:
		if phrase in text:
			return False

	return True

# Detects any countries mentioned in tweet
def detect_country(text):
	countries = list(geotext.GeoText(i).country_mentions)
	cities = list(geotext.GeoText(i).cities)

	# If any countries are detected, returns them
	if len(countries)>0 and len(cities)==0:
		# Converts each country code to the countries name (e.g. CA-->Canada)
		names = ""
		for c in countries:
			names = names + pycountry.countries.get(alpha_2=c).name + " "
			#print(pycountry.countries.get(alpha_2=c).name)
		return names
	# If no countries mentioned
	return "N/A"

# Reads TSV file and extracts text from each tweet
tweets = []
with open("tweets.tsv", "r", newline="") as fp:
	read_tsv = csv.reader(fp, delimiter="\t")
	for i in read_tsv:
		if i[12]!="text":
			tweets.append(i[12])

# TODO Start doing live sentament analysis and track price of BTC in various geographies. Then, after 1 week (or more) see if there's a correlation between my sentiment analysis and BTC price
# TODO Replace geotext country search with custom solution: make list of all countries and their top 5-10 cities, compare each tweet aginst this list to extract geographic info
# TODO replace current TSV solution with Google Sheets "database" solution (see: https://www.youtube.com/watch?v=vISRn5qFrkM)
# TODO find a way of getting all text from tweets (no "..." at end of text)

# Iterates over all tweets
for i in tweets:
	#'''
	try:
		if detect_country(i)!="N/A":
			print(i)
			print(s.sentiment(i)[0])
			print("Countries Mentioned:", detect_country(i))
			print("===========================================")
	except:
		pass
	'''
	# If tweet passes screening, prints out its contents
	i_lower = i.lower()
	if screen_tweets(i_lower):
		# Calculates sentiment
		sentiment = s.sentiment(i)

		# Only displays text if all 7 algorithms come to same conclusion (7 POSITIVE or 7 NEGATIVE)
		if sentiment[1]==1:
			# Prints text, sentiment (positive/negative), and any countries mentioned
			
			print(i)
			print(sentiment[0])
			print("Countries Mentioned:", detect_country(i))
			print("=========================================")
			'''