import re # A python library used for regular expressions

import tweepy # Twitter library used to pull tweets

from tweepy import OAuthHandler # Used to authenticate the user of twitter’s API

from textblob import TextBlob # Used to process text data

class TwitterClient():

    def __init__(self):
    # keys and tokens from the Twitter Dev Console
    # Class constructor or init method
        consumer_key = 'oAlgfrCWUEeeTx5NjFVafFRD5'
        consumer_secret = '0iK62u1itNcTT9QGUfrzfpt2x1JfjbBx72Hc4rvxplyGsUNqWA'
        access_token = '803517278-WmqLmdAM9xpqDQrQZTzA8Or7H4FAK05yy0UvnoUc'
        access_token_secret = 'dGIr6gRhSz9EwHpmOHg2ioUZXNwr8nyjswNqaUiq17C6N'

        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        '''
        Utility function to clean tweet text by removing links, special chars
        using simple regex statements
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_polarity(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set polarity
        return analysis.sentiment.polarity

    def get_tweet_sentiment(self, tweet):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create  TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if (analysis.sentiment.polarity > 0):
            return 'positive'
        elif (analysis.sentiment.polarity == 0):
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        '''
        Main function to fetch tweets and parse them
        '''
        # empty list to store parsed tweets
        tweets = []
        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)
            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of a tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                # save polarity as well
                parsed_tweet['polarity'] = self.get_tweet_polarity(tweet.text)
                # appending parsed tweet to tweets list
                if (tweet.retweet_count > 0):
                    # if tweet has retweets, ensure that it is appended only once
                    if (parsed_tweet not in tweets):
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
                    # return parsed tweets
                    return tweets
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
            
def main():
    # creating object of TwitterClient Class
    api = TwitterClient()
    # calling function to get tweets
    tweets = api.get_tweets(query = 'memes', count = 200)
    # picking positive tweets from tweets
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {}%".format(100*len(ptweets)/len(tweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    # percentage of neutral tweets
    check = len(tweets) - len(ntweets) - len(ptweets)
    print("Neutral tweets percentage: {} %".format(100*(check/len(tweets))))
    # printing first 5 positive tweets
    print("\n\nPositive tweets: ")
    for tweet in ptweets[:10]:
        print((tweet['text'] + "  Rating: " + str(tweet['polarity'])))
        # printing first 5 negative tweets
    print("\n\nNegative tweets: ")
    for tweet in ntweets[:10]:
        print((tweet['text'] + "  Rating: " + str(tweet['polarity'])))

if __name__ == "__main__":
    # calling main function
    main()
