import tweepy
from twitter_keys import api_key, api_secret, consumer_key, consumer_secret, access_token, access_token_secret, bearer_token

# Initialize Tweepy client
client = tweepy.Client(
    consumer_key =api_key,
    consumer_secret =api_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
)

media_path = 'pictures/bug.jpg'
#auth.set_access_token(twitter_keys.access_token, twitter_keys.access_token_secret)
tweet_text = 'This was tweeted with Python'
try:
        response = client.create_tweet(text=tweet_text)
        print("Tweet posted successfully!")
        print(f"Tweet ID: {response.data['id']}")
        print(f"Tweet Text: {response.data['text']}")
except tweepy.TweepyException as e:
        print(f"Error posting tweet: {e}")