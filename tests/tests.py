import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/home/spyros_gew/MyScrabble/code')))
import scrabble

class MockPlayer:
  def __init__(self, letters):
      self.active_letters = letters

  def get_active_letters(self):
      return self.active_letters

  def set_active_letters(self, letters):
      self.active_letters = letters

class TestCheckLetters(unittest.TestCase):

  def test_valid_word(self):
      player = MockPlayer(['H', 'E', 'L', 'L', 'O'])
      result = check_letters(None, "HELLO", player)
      self.assertTrue(result)
      self.assertEqual(player.get_active_letters(), [])  # All letters used up

  def test_one_missing_letter_with_wildcard(self):
      player = MockPlayer(['H', 'E', 'L', '*', 'O'])
      result = check_letters(None, "HELLO", player)
      self.assertTrue(result)
      self.assertEqual(player.get_active_letters(), [])  # Wildcard used

  def test_one_missing_letter_without_wildcard(self):
      player = MockPlayer(['H', 'E', 'L', 'O'])
      result = check_letters(None, "HELLO", player)
      self.assertFalse(result)

  def test_two_missing_letters_with_wildcards(self):
      player = MockPlayer(['H', 'E', 'L', '*', '*'])
      result = check_letters(None, "HELLZ", player)
      self.assertTrue(result)
      self.assertEqual(player.get_active_letters(), [])  # Two wildcards used

  def test_two_missing_letters_without_wildcards(self):
      player = MockPlayer(['H', 'E', 'L', 'O'])
      result = check_letters(None, "HELLZ", player)
      self.assertFalse(result)

  def test_more_than_two_missing_letters(self):
      player = MockPlayer(['H', 'E'])
      result = check_letters(None, "HELLO", player)
      self.assertFalse(result)

if __name__ == '__main__':
  unittest.main()