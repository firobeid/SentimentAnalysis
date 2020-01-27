# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 23:23:12 2018

Modified and commented by: Firas Obeid
Email: feras.obeid@lau.edu
"""
# First I applied for an account activity API(application programming interface) on Twitter
# Installed in conda env the following: "python -m textblob.download_corpora" to analyze large textual data 
import re # refers to regular expression that is a set of characters that help find certain strings or tweets in our case
import tweepy # Installed this library in conda env; its the client for the Twitter API
from tweepy import OAuthHandler # This will redirect us to twitter.com to authorize our application. We will use it to pass our consumer token and secret
from textblob import TextBlob 

class TwitterClient(object): # Define a class which is a template, called "TwitterClient"
	''' 
	Generic Twitter Class for sentiment analysis. 
	'''
	def __init__(self): 
		''' 
		Class constructor or initialization method. 
		'''
		# keys and tokens from the Twitter Dev Console 
		consumer_key = 'GUnlUI21y2Q57gtKWo5NG0ffC' # These are used for authorizing python with the Twitter API
		consumer_secret = '9tFt1HlB50uo59tGrKkfs3qLRnDC3q0SIe2FjDw0kOjry0qBau'
		access_token = '1050147431046889472-IbzEPNtVyBkFJmWF6RqnNQyv32OOXO'
		access_token_secret = 'YsCeipVK9uAG0TF2veENRYgvZvzlOnKkSoYGdLspXQSPE'

		# attempt authentication 
		try: 
			# create OAuthHandler object 
			self.auth = OAuthHandler(consumer_key, consumer_secret) 
			# set access token and secret 
			self.auth.set_access_token(access_token, access_token_secret) 
			# create tweepy API object to fetch tweets 
			self.api = tweepy.API(self.auth) 
		except: 
			print("Error: Authentication Failed") # error message incase tokens or keys are invalid 

	def clean_tweet(self, tweet): 
		''' 
		Utility function to clean tweet text by removing links, special characters 
		using simple regex statements. 
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()) 

	def get_tweet_sentiment(self, tweet): 
		''' 
		Utility function to classify sentiment of passed tweet 
		using textblob's sentiment method 
		'''
		# create TextBlob object of passed tweet text 
		analysis = TextBlob(self.clean_tweet(tweet)) # The clean_tweet methode will clean the tweets from special characters
		# pass set sentiment to the text (tokens) and classify according to polarity                              Words will be split from the body text and remoce stop words (I, you...)
		if analysis.sentiment.polarity > 0:                                     # The isolated texts are tagged and special text(tokens) are selected. 
			return 'positive'                                                    # All of this is done via textblob                
		elif analysis.sentiment.polarity == 0:        
			return 'neutral'   
		else: 
			return 'negative'

	def get_tweets(self, query, count = 10): # We are fetching th tweets from the API. Self parameter always inside a function that is inside a class
		'''                                   
		Main function to fetch tweets and parse them. 
		'''
		# empty list to store parsed tweets 
		tweets = [] 

		try: 
			# call twitter api to fetch tweets 
			fetched_tweets = self.api.search(q = query, count = count) 

			# parsing tweets one by one 
			for tweet in fetched_tweets: 
				# empty dictionary to store required params of a tweet 
				parsed_tweet = {} #storing pure text 

				# saving text of tweet 
				parsed_tweet['text'] = tweet.text 
				# saving sentiment of tweet 
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 

				# appending parsed tweet to tweets list 
				if tweet.retweet_count > 0: 
					# if tweet has retweets, ensure that it is appended only once  #important
					if parsed_tweet not in tweets: 
						tweets.append(parsed_tweet) 
				else: 
					tweets.append(parsed_tweet) 

			# return parsed tweets 
			return tweets 

		except tweepy.TweepError as e: 
			# print error (if any) 
			print("Error : " + str(e)) 
print("\n\t\t\t Welcome to the Sentiment Analysis on Latest Twitter Feeds!")

def last(keyword,tweets_nb): # outside the class we code a funtion to analyze the sentiments using statistical approach
	# creating object of TwitterClient Class. This function will pass the end output of the whole program once called 
	api = TwitterClient() 
	# calling function to get tweets 
	tweets = api.get_tweets(query = str(keyword), count = int(tweets_nb)) 

	# picking positive tweets from tweets 
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
	
	# picking negative tweets from tweets 
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	plist = []
	for tweet in ptweets[:10]: 
		plist.append(tweet["text"])
	nlist = []	
	for tweet in ntweets[:10]: 
		nlist.append(tweet["text"]) 
	return tweets, ptweets, ntweets, plist, nlist

'''
    # percentage of positive tweets 
	print("\n\nPositive tweets percentage: {} %".format(round(100*len(ptweets)/len(tweets), 4))) 
	# percentage of negative tweets 
	print("Negative tweets percentage: {} %".format(round(100*len(ntweets)/len(tweets), 4))) 
	# percentage of neutral tweets  
	print("Neutral tweets percentage: {} %".format(round(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets),4))) 

	# printing first 10 positive tweets 
	print("\n\nPositive tweets(Showing only 10 tweets):\n\n") 
	for tweet in ptweets[:10]: 
		print("+++ ",tweet['text']) 

	# printing first 10 negative tweets 
	print("\n\nNegative tweets(Showing only 10 tweets):\n\n") 
	for tweet in ntweets[:10]: 
		print("---  ",tweet['text']) 
        
def user(tweet,number_of_tweets):
    while True:
        try:
            tweet = str(input('\n\n\n\n\n\n\nPlease input the Tweet term (i.e. AAPL, Trump, Natural Gas, Bitcoin...): '))
            pass
        except ValueError:
            print("Oops!  That was no valid word to search for.  Try again...")
        try:
            number_of_tweets = int(input('Please enter the number of tweets to run over live search(i.e. 1000,10000...): '))
            break
        except ValueError:
            print("Oops!  That was no valid number to search for.  Try again and just enter digits...")
    return last(tweet,number_of_tweets)   
'''
if __name__ == "__main__":  # to set main() function as the main function to run at the end and if the module is imported from another script
	# calling main function will only run as the end output to the whole code 
	last() 
