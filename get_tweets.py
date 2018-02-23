#!/usr/bin/python3

import tweepy
import csv
import get_creds
# Twitter API keys/secrets
consumer_key, consumer_secret, access_token, access_token_secret = get_creds.get_creds(1)

def create_csv(tweet_json):
	headings = [i for i in tweet_json]
#	print(headings)

def main():
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)	# API class
	crypto_tweets = tweepy.Cursor(api.search, q="Bitcoin").items(1)

	for tweet in crypto_tweets:
#		print(tweet.id_str, tweet.created_at, tweet.text)
		#print(tweet._json)
		create_csv(tweet._json)
		for i in tweet._json:
			print(i, tweet._json[i])

if __name__ == '__main__':
	main()