import requests
import pandas as pd

auth = requests.auth.HTTPBasicAuth('<CLIENT_ID>', '<SECRET_TOKEN>')

data = {'grant_type': 'password',
        'username': '<USERNAME>',
        'password': '<PASSWORD>'}

headers = {'User-Agent': 'MyBot/0.0.1'}

res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

TOKEN = res.json()['access_token']

headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

res = requests.get("https://oauth.reddit.com/r/python/hot",
                   headers=headers)

df = pd.DataFrame()

for post in res.json()['data']['children']:
    # append relevant data to dataframe
    df = df.concat({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['score']
    }, ignore_index=True)

print(df)

