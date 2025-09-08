import math
from datetime import date
from logging import exception

import psycopg2
import tweepy
from twitter_keys import api_key, api_secret, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token
import datetime

debug = True


# Initialize Tweepy client
client = tweepy.Client(
    consumer_key =api_key,
    consumer_secret =api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)
def tweet_builder(tweet_datetime):
    return_string = "test tweet"
    # Connect to database, grab day & month
    conn = psycopg2.connect(host="localhost", dbname="tweets", user="postgres", password="corndog", port=5432)
    cursor = conn.cursor()
    month = tweet_datetime.month
    day = tweet_datetime.day
    year = tweet_datetime.year
    # Query for tweet text
    query = """SELECT * FROM tweet WHERE date_month = %s AND date_day = %s;"""
    cursor.execute(query, (month, day))
    rows = cursor.fetchall()
    # Pick a tweet if there are multiple for the same day

    if len(rows) == 0:
        raise(RuntimeError("No tweet found for this date"))
    choice = year % len(rows)
    tweet_info = rows[choice]
    print(tweet_info[5])
    if tweet_info[5] == "NaN":
        raise(RuntimeError("Tweet text is empty for this date"))

    tweet_text = tweet_info[5] + " - " + tweet_info[7]
    print(tweet_text)

    # Close connections
    cursor.close()
    conn.close()
    return return_string

#media_path = 'pictures/bug.jpg'
def post_plain_tweet(tweet_text):
    if debug:
        print(tweet_text)
        return 0
    try:
            response = client.create_tweet(text=tweet_text)
            print("Tweet posted successfully!")
            print(f"Tweet ID: {response.data['id']}")
            print(f"Tweet Text: {response.data['text']}")
            return 0
    except tweepy.TweepyException as e:
            print(f"Error posting tweet: {e}")
            return e

def get_tweet_text(self):
    today = date.today()
    # hook up to postgres database
try:
    if debug:
        tweet_string = tweet_builder(date(2025, 1, 13))
        #tweet_string = tweet_builder(date(2018, 1, 3))
    else:
        tweet_string = tweet_builder(date.today())

    post_plain_tweet(tweet_string)
except Exception as e:
    print("Error generating tweet: " + str(e))


