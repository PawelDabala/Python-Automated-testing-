import json
import os
import re
from urllib.parse import urljoin

# import requests
from pip._vendor import requests

USERS_API = "https://api.github.com/users/"

class Twitter:
    version = '1.0'
    #plik textowy zostje przekazany jako backend
    def __init__(self, backend=None, username=None):
        self.backend = backend
        self._tweets = []
        self.username = username

    @property
    def tweets(self):
        #jeżeli plik backend jest zadeklarowany i chcemy przekazać nasze tweety
        if self.backend and not self._tweets:
            backend_text = self.backend.read()
            if backend_text:
                self._tweets = json.loads(backend_text)
        return self._tweets

    @property
    def tweet_messages(self):
        return [tweet['message'] for tweet in self.tweets]

    def get_user_avatar(self):
        if not self.username:
            return None

        url = urljoin(USERS_API, self.username)
        resp = requests.get(url)
        return resp.json()['avatar_url']

    def tweet(self, message):
        if len(message) > 160:
            raise Exception('Message too long')
        self.tweets.append({'message': message,
                            'avatar': self.get_user_avatar(),
                            'hashtags': self.find_hashtags(message)
                            })
        #jeżeli tweetujemy i nasz backend istnieje prubujemy zapisać do niego kopie naszych
        #tweets
        if self.backend:
            self.backend.write(json.dumps(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]


    def get_all_hastags(self):
        hashtags = []
        for message in self.tweets:
            hashtags.extend(message['hashtags'])
        if hashtags:
            return set(hashtags)

        return "No hashtags found"

