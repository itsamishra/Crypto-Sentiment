#!/usr/bin/python3

import tweepy
import csv
import get_creds
# Twitter API keys/secrets
consumer_key, consumer_secret, access_token, access_token_secret = get_creds.get_creds(1)

# Headings of TSV file
headings = ["contributors", "favorite_count", "retweeted_status", "retweet_count", "extended_entities", "geo", "in_reply_to_screen_name", "metadata", "lang", "user", "in_reply_to_status_id_str", "coordinates", "text", "place", "in_reply_to_user_id_str", "favorited", "truncated", "source", "possibly_sensitive", "is_quote_status", "id_str", "retweeted", "in_reply_to_user_id", "id", "created_at", "in_reply_to_status_id", "entities"]

# Number of tweets to retreive
NUM_TWEETS = 2000

# Writes new tweet to TSV file
def write_to_tsv(tweet_json):
	# Gets data in array format
	data = []
	for i in headings:
		try:
			data.append(tweet_json[i])
		except:
			data.append(" ")

	# Appends data to end of TSV file
	with open("tweets.tsv", "a", newline="") as fp:
		csv_writer = csv.writer(fp, delimiter="\t")
		csv_writer.writerows([data])


def main():
	# Creates API object using proper authentication
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)

	# Creates search query
	crypto_tweets = tweepy.Cursor(api.search, q="Bitcoin").items(NUM_TWEETS)

	# Iterates over searched values
	count = 0
	for tweet in crypto_tweets:
		write_to_tsv(tweet._json)

		# Prints progress
		count+=1
		print(str(100*count/NUM_TWEETS) + " % completed")

if __name__ == "__main__":
	main()