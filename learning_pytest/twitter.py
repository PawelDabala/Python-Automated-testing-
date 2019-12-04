import os
import re


class Twitter:
    version = '1.0'
    #plik textowy zostje przekazany jako backend
    def __init__(self, backend=None):
        self.backend = backend
        self._tweets = []

    @property
    def tweets(self):
        #jeżeli plik backend jest zadeklarowany i chcemy przekazać nasze tweety
        if self.backend and not self._tweets:
            self._tweets = [line.rstrip('\n') for line in self.backend.readlines()]
        return self._tweets

    def tweet(self, message):
        if len(message) > 160:
            raise Exception('Message too long')
        self.tweets.append(message)
        #jeżeli tweetujemy i nasz backend istnieje prubujemy zapisać do niego kopie naszych
        #tweets
        if self.backend:
            self.backend.write("\n".join(self.tweets))

    def find_hashtags(self, message):
        return [m.lower() for m in re.findall("#(\w+)", message)]
