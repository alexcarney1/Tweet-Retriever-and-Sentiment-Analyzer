#
# Author: Alex R. Carney
# Summary: Fetch, analyze, and store tweets between 2 input dates without many of the limitations
#of the Twitter API. Can typically retrieve 12,000 tweets before reaching a HTTP 429 server cool-down. 
# Sentiment analysis also captured for data analytics. Fetched tweets stored in a .csv file.
#
# ****Links to neccessary libraries****
# GetOldTweets3: https://pypi.org/project/GetOldTweets3/
# tweet-preprocessor: https://pypi.org/project/tweet-preprocessor/
# textblob: https://textblob.readthedocs.io/en/dev/
#
import GetOldTweets3 as got
import csv
import pandas as pd
from textblob import TextBlob
import preprocessor as p
import time 

def disclaimers():
    print("Alex R. Carney, 3/28/2020 \nRetrieving excessive amounts of tweets may result"
          " in HTTP 429 Errors (server rate limit exceeded).\n")
    
def read_user_input():      
    query = input("Enter twitter search query you wish to retrieve: ")
    startDate = input("Enter the start date in this format yyyy-mm-dd: ")
    endDate = input("Enter the end date (upper bound, not included) in this format yyyy-mm-dd: ")
    tweetsPerDay= int(input("Retrieve how many tweets per day? "))
    allDates = pd.date_range(start= startDate, end= endDate).strftime('%Y-%m-%d').tolist()
    return query, tweetsPerDay, allDates

def clean_tweet(tweet):
    return p.clean(tweet)

def analyze_sentiment(tweet):
    analysis = TextBlob(tweet) 
    return analysis.sentiment.polarity
    
def main():
    disclaimers()
    query, tweetsPerDay, allDates = read_user_input()
    print("working...")
    i= 0
    with open(query+'.csv', "a", newline = '') as csvFile:
        csvWriter = csv.writer(csvFile)
        for day in range(0,len(allDates)-1): 
            
            tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query)\
            .setSince(allDates[day]).setUntil(allDates[day+1]).setMaxTweets(tweetsPerDay)
            
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)                     
            for tweet in tweets:
                cleanTweet = clean_tweet(tweet.text)
                i+=1
                print(str(i) + " tweets collected :)")         
                sentimentScore = analyze_sentiment(cleanTweet)
                csvWriter.writerow([tweet.date,sentimentScore,cleanTweet.encode('utf-8')])   
        
        print ("Scraped tweets saved to: " + query + '.csv')
main()
