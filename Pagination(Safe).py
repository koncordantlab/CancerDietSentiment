import requests
import urllib.parse
import pandas as pd
import os
import time

bearer_token = 'acquire your own'


def get_tweets(query, max_results, next_token=None):
    url = f"https://api.twitter.com/2/tweets/search/recent?query={query}&max_results={max_results}"
    if next_token:
        url += f"&next_token={next_token}"
    
    headers = {
        'Authorization': f'Bearer {bearer_token}',
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def parse_tweets(tweetList):
    if tweetList is None:
        print("No response received.")
        return []
    #tweets = response.get('data', [])
    parsed_tweets = []   
    for tweet in tweetList:
        if 'extended_tweet' in tweet:
            parsed_tweets.append(tweet['extended_tweet']['full_text'])
        elif 'retweeted_status' in tweet:
            parsed_tweets.append(tweet['retweeted_status']['text'])
        elif 'quoted_status' in tweet:
            parsed_tweets.append(tweet['quoted_status']['text'])
        else:
            parsed_tweets.append(tweet['text'])
    return parsed_tweets

def save_to_file(queries, max_results, num_pages):
    for i in range(len(queries)):
        tweets_data = []
        next_token = None
        page_count = 0

        while page_count < num_pages: #and x-rate-limit-remaining > max_results:
            response = get_tweets(queries[i], max_results, next_token)
            if response and 'data' in response:
                tweets_data.extend(response['data'])
                next_token = response['meta'].get('next_token')
                page_count += 1
                if not next_token:
                    break
            else:
                break
            time.sleep(1)

        parsed_tweets = parse_tweets(tweets_data)

        #Keep only the unique tweets
        unique_tweets = list(set(parsed_tweets))


        # Check if the file exists and read existing data
        if os.path.exists("tweets5.xlsx"):
            existing_df = pd.read_excel("tweets5.xlsx")
            existing_tweets = existing_df["Tweet"].tolist()
            combined_tweets = list(set(existing_tweets + unique_tweets))
        else:
            combined_tweets = unique_tweets

        # Create a DataFrame with the combined tweets
        combined_df = pd.DataFrame(combined_tweets, columns=["Tweet"])

        # Save the DataFrame to the Excel file
        combined_df.to_excel("tweets5.xlsx", index=False)
        print(f"Pulled {len(tweets_data)} tweets, Non-repeat {len(unique_tweets)}, total {len(combined_tweets)} , Completed {page_count} pages")
    print("tweets excel made")

    


queries = ['(cancer food) lang:en -is:retweet', '(cancer sugar) lang:en -is:retweet','(cancer diet) lang:en -is:retweet','(anti-cancer diet) lang:en -is:retweet','(cancer food) lang:en -is:retweet' ]
max_results = 100
num_pages = 4

save_to_file(queries, max_results, num_pages)