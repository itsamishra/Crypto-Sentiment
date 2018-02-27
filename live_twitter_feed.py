from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import get_creds
import json
import geotext
import pycountry
import sentiment_mod as s
import time
from save_tweet import add_to_db


# TODO Add SQLite support to save sentiment
# TODO Change country return string from "name" to "alpha_2"
# TODO Start doing live sentament analysis and track price of BTC in various geographies. Then, after 1 week (or more) see if there's a correlation between my sentiment analysis and BTC price
# TODO Replace geotext country search with custom solution: make list of all countries and their top 5-10 cities, compare each tweet aginst this list to extract geographic info
# TODO replace current TSV solution with Google Sheets "database" solution (see: https://www.youtube.com/watch?v=vISRn5qFrkM)
# TODO find a way of getting all text from tweets (no "..." at end of text)


# Twitter API keys/secrets
consumer_key, consumer_secret, access_token, access_token_secret = get_creds.get_creds(1)

# Keeps track of positive/negative for each country
country_stats = {}

# Returns country referenced in text
def detect_country(text):
	countries = list(geotext.GeoText(text).country_mentions)
	cities = list(geotext.GeoText(text).cities)

	# If any countries are detected, returns them (ignores text with city names because some cities have stupid names like "Of")
	if len(countries)>0 and len(cities)==0:
		# Converts each country code to the countries name (e.g. CA-->Canada)
		country_names = []
		for c in countries:
			country_names.append(pycountry.countries.get(alpha_2=c).name)

		return country_names

	# If no countries mentioned
	return []

# Screens tweets
def tweet_screening(text):
	# Removes retweets or reply tweets
	if text[0:2]=="RT" or text[0]=="@":
		return False

	return True

def get_stats(country, sentiment):
	if country not in country_stats.keys():
		country_stats[country] = [0,0,0]
	
	if sentiment[0]=="pos":
		country_stats[country][0] += sentiment[1]
	else:
		country_stats[country][1] += sentiment[1]

	country_stats[country][2] += 1

class listener(StreamListener):

	def on_data(self, data):
		all_data = json.loads(data)

		# If tweet passes screening, print it
		if tweet_screening(all_data["text"]):
			detected_countries = detect_country(all_data["text"])

			# If more than 0 countries are found in tweet, print the tweet
			if len(detected_countries)!=0:
				print(all_data["text"])
				print("Countries:", detected_countries)

				sentiment = s.sentiment(all_data["text"])
				print(sentiment)

				for c in detected_countries:
					get_stats(c, sentiment)
				print(country_stats)
				print("-------------------------------------------------------------------------------")

				# Saves tweet sentiment info to db
				current_time = str(time.time())
				tweet_id = all_data["id_str"]

				for c in detected_countries:
					if sentiment[0]=="pos":
						add_to_db("sentiment_db", c, current_time, tweet_id, sentiment[1], 0)
					else:
						add_to_db("sentiment_db", c, current_time, tweet_id, 0, sentiment[1])

				return True

	def on_error(self, status):
		print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())

# Mysterious error requires this try/except. Error is: KeyError: 'UK' (see mysterious_error.txt for more info)
try:
	twitterStream.filter(track=["bitcoin"])
except Exception as e:
	print(e)