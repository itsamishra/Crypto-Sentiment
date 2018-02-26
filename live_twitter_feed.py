from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import get_creds
import json
import geotext
import pycountry

# Twitter API keys/secrets
consumer_key, consumer_secret, access_token, access_token_secret = get_creds.get_creds(1)

# Returns country referenced in text
def detect_country(text):
	countries = list(geotext.GeoText(text).country_mentions)
	cities = list(geotext.GeoText(text).cities)

	# If any countries are detected, returns them (ignores text with city names because some cities have stupid names like "Of")
	if len(countries)>0 and len(cities)==0:
		# Converts each country code to the countries name (e.g. CA-->Canada)
		names = ""
		for c in countries:
			names = names + pycountry.countries.get(alpha_2=c).name + " "
			#print(pycountry.countries.get(alpha_2=c).name)
		return names
	# If no countries mentioned
	return "N/A"

# Screens tweets
def tweet_screening(text):
	# Removes retweets or reply tweets
	if text[0:2]=="RT" or text[0]=="@":
		return False

	# Only considers tweets that reference countries
	country_names = detect_country(text)
	if country_names=="N/A":
		return False

	return True

class listener(StreamListener):

	def on_data(self, data):
		all_data = json.loads(data)
		if tweet_screening(all_data["text"]):
			print(all_data["text"])
			print("Countries:", detect_country(all_data["text"]))
			print("-------------------------------------------------------------------------------")

			return True

	def on_error(self, status):
		print(status)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["bitcoin"])