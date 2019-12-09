import pytest
from unittest.mock import patch, Mock, MagicMock
from twitter import Twitter


class ResponseGetMock(object):
    def json(self):
        return {'avatar_url': 'test'}


# nowy fixture który blokuje requesty
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

    # def monkey_return():
    #     return 'test'
    #
    # monkeypatch.setattr(twitter, 'get_user_avatar', monkey_return)

    return twitter


def test_twitter_initialization(twitter):
    assert twitter


@patch.object(Twitter, 'get_user_avatar', return_value='test')
def test_tweet_single_message(avatar_mock, twitter):
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


@patch.object(Twitter, 'get_user_avatar', return_value='test')
def test_tweet_with_username(avatar_mock, twitter):
    if not twitter.username:
        pytest.skip()

    twitter.tweet('Test message')
    assert twitter.tweets == [{'message': 'Test message', 'avatar': 'test', 'hashtags': []}]
    avatar_mock.assert_called()


def test_tweet_with_hashtag_mock(twitter):
    # zatwitowaliśmy wiadomosć 'Test #seconed' znalezionym hastagiem powinno
    # by second nadpisaliśmy widadomość korzystajac z obiektu Mock() i wymuśiliśmy zwracana wiadomoćś w ['first']
    twitter.find_hashtags = Mock()
    twitter.find_hashtags.return_value = ['first']
    twitter.tweet('Test #second')
    assert twitter.tweets[0]['hashtags'] == ['first']
    twitter.find_hashtags.assert_called_with('Test #second')


def test_twitter_version(twitter):
    #MagicMock używamy w celu nadpisania metod magicznych w pythonie
    twitter.version = MagicMock()
    #metoda __eq__ odpowiada za porównanie do jakiejś wartości
    twitter.version.__eq__.return_value = '2.0'
    assert twitter.version == '2.0'



def test_twitter_get_all_hashtags(twitter):
    twitter.tweet('Test #first')
    twitter.tweet('Test #first #second')
    twitter.tweet('Test #third')
    assert twitter.get_all_hashtags() == {'first', 'second', 'third'}

def test_twitter_get_all_hashtags_not_found(twitter):
    twitter.tweet('Test first')
    assert twitter.get_all_hashtags() == "No hashtags found"
