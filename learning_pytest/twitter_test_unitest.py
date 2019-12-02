import unittest

from learning_pytest.twitter import Twitter


class TwitterTest(unittest.TestCase):
    def setUp(self):
        self.twitter = Twitter()
    def test_initizalization(self):
        self.assertTrue(self.twitter) #sprawdz czy klasa istnieje

    def test_tweet_single(self):
        # Zazwyczaj przy testach zachodzą trzy przypadki:
        # Given - sytuacje wejściową
        # twitter = Twitter()
        # When - wykonywanie akcji na tej sytuacji
        self.twitter.tweet('Test message')
        # Then - sprawdzenie wyników
        self.assertEqual(self.twitter.tweets, ['Test message'])




if __name__=='__main__':
    unittest.main()
