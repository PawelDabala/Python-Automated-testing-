import pytest
from twitter import Twitter


def test_twitter_initialization():
    twitter = Twitter()
    assert twitter


def test_tweet_single_message():
    twitter = Twitter()
    twitter.tweet('Test message')
    assert twitter.tweets == ['Test message']


def test_tweet_long_message():
    twitter = Twitter()
    with pytest.raises(Exception):
        twitter.tweet('test' * 41)
    assert twitter.tweets == []

@pytest.mark.parametrize("message, hashtag",(
                         ("Test #first message", "first"),
                         ("#first Test message", "first"),
                         ("#FIRST Test message", "FIRST")
                         ))
def test_tweet_with_hashtag(message, hashtag):
    twitter = Twitter()
    assert hashtag in twitter.find_hashtags(message)




