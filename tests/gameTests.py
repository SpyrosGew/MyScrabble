import unittest
import sys
import os

# Add the directory of your scrabble code to the path so we can import the scrabble module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/home/spyros_gew/MyScrabble/code')))
import scrabble  # Now we can access everything from the scrabble module


class MockPlayer:
    def __init__(self, active_letters):
        self.active_letters = active_letters
    
    def set_active_letters(self, active_letters):
        self.active_letters = active_letters

    def get_active_letters(self):
        return self.active_letters

class TestGame(unittest.TestCase):

    def test_valid_word(self):
        g = scrabble.Game()
        player = MockPlayer(['H', 'E', 'L', 'L', 'O'])
        result = g.check_letters("HELLO", player)  # Use scrabble.check_letters
        self.assertTrue(result)
        self.assertEqual(player.get_active_letters(), [])  # All letters used up

    def test_one_missing_letter_with_wildcard(self):
        g = scrabble.Game()
        player = MockPlayer(['H', 'E', 'L', '*', 'O'])
        result = g.check_letters("HELLO", player)  # Use scrabble.check_letters
        self.assertTrue(result)
        self.assertEqual(player.get_active_letters(), [])  # Wildcard used

    def test_one_missing_letter_without_wildcard(self):
        g = scrabble.Game()
        player = MockPlayer(['H', 'E', 'L', 'O'])
        result = g.check_letters("HELLO", player)  # Use scrabble.check_letters
        self.assertFalse(result)

    def test_two_missing_letters_without_wildcards(self):
        g = scrabble.Game()
        player = MockPlayer(['H', 'E', 'L', 'O'])
        result = g.check_letters("HELLZ", player)  # Use scrabble.check_letters
        self.assertFalse(result)

    def test_more_than_two_missing_letters(self):
        g = scrabble.Game()
        player = MockPlayer(['H', 'E'])
        result = g.check_letters("HELLO", player)  # Use scrabble.check_letters
        self.assertFalse(result)
    
    

if __name__ == '__main__':
    unittest.main()
