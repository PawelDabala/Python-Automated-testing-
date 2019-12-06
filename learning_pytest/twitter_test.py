import pytest
from _pytest import monkeypatch
from twitter import Twitter


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}

#nowy fixture który blokuje requesty
# @pytest.fixture(autouse=True)
# def no_requests(monkeypatch):
#     korzystajac z monkeypatch usuneliśy request, zaden request nie zostanie wykorzystany z naszych
#     testach.
#     monkeypatch.delattr('requests.sessions.Session.request')


@pytest.fixture
def backend(tmpdir):
    temp_file = tmpdir.join('test.txt')
    temp_file.write('')
    return temp_file


@pytest.fixture(params=[None, 'python'])
def username(request):
    return request.param


@pytest.fixture(params=['list', 'backend'], name='twitter')
def fixture_twitter(backend, username, request, monkeypatch):
    if request.param == 'list':
        twitter = Twitter(username=username)
    elif request.param == 'backend':
        twitter = Twitter(backend=backend, username=username)

    def monkey_return():
        return 'test'

    monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return)

    return twitter


def test_twitter_initialization(twitter):
    assert twitter


def test_tweet_single_message(twitter):
    twitter.tweet('Test message')
    assert twitter.tweet_messages == ['Test message']


def test_tweet_long_message(twitter):
    with pytest.raises(Exception):
        twitter.tweet('test' * 41)
    assert twitter.tweet_messages == []


def test_initialize_two_twitter_classes(backend):
    twitter1 = Twitter(backend=backend)
    twitter2 = Twitter(backend=backend)

    twitter1.tweet('Test 1')
    twitter2.tweet('Test 2')

    assert twitter2.tweet_messages == ['Test 1', 'Test 2']


@pytest.mark.parametrize("message, expected", (
        ("Test #first message", ["first"]),
        ("#first Test message", ["first"]),
        ("#FIRST Test message", ["first"]),
        ("Test message #first", ['first']),
        ("Test message #first #second", ["first", "second"])
))
def test_tweet_with_hashtag(twitter, message, expected):
    assert twitter.find_hashtags(message) == expected  # dorbra praktyka nazywanie


def test_tweet_with_username(twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test'}]