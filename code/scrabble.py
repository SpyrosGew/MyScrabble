import random
import threading
import select
import time
import twl
import sys
# DICTIONARIES - - - - - - -

# - VALUE DICTIONARY - - - -
letter_value = {
  "A": 1,
  "B": 3,
  "C": 2,
  "D": 1,
  "E": 1,
  "F": 3,
  "G": 3,
  "H": 3,
  "I": 1,
  "J": 7,
  "K": 5,
  "L": 4,
  "M": 2,
  "N": 1,
  "O": 1,
  "P": 3,
  "Q": 6,
  "R": 1,
  "S": 1,
  "T": 1,
  "U": 2,
  "V": 4,
  "W": 4,
  "X": 6,
  "Y": 4,
  "Z": 7,
  "*": 0
}
# - COUNT DICTIONARY - - - -
letter_bag = {
  "A": 9,
  "B": 2,
  "C": 2,
  "D": 4,
  "E": 12,
  "F": 2,
  "G": 3,
  "H": 2,
  "I": 9,
  "J": 1,
  "K": 1,
  "L": 4,
  "M": 2,
  "N": 6,
  "O": 8,
  "P": 2,
  "Q": 1,
  "R": 6,
  "S": 4,
  "T": 6,
  "U": 4,
  "V": 2,
  "W": 2,
  "X": 1,
  "Y": 2,
  "Z": 1,
  "*": 2
}
#END OF DICTIONARIES - - - -

# CLASSES - - - - - - - -

# - PLAYER CLASS - - - - - { can update active letters }
class Player:

  # - - CONSTRUCTOR - - - - -
  def __init__(self, name, value):
    self.name = name     #the players name
    self.value = value   #is he player 0 or 1?
    self.active_letters = [] # a list of his 7 active letters
    self.letter_changes = 3 # how many letter changes he has left

  # - - GETTERS - - - - - - - - - - -
  def get_active_letters(self):
    return self.active_letters

  def get_letter_changes(self):
    return self.letter_changes

  def get_name(self):  
    return self.name


  def get_value(self):
    return self.value

  # - - SETTERS - - - - - - - - - - -
  def set_active_letters(self, active_letters):
    self.active_letters = active_letters

  def set_name(self, name):
    self.name = name

  def set_letter_changes(self, letter_changes):
    self.letter_changes = letter_changes

  # - - FUNCTIONS - - - - - - - - - - -
  def update_active_letters(self, bag):  
    new_letters = bag.draw_letters(7 - len(self.active_letters))
    self.active_letters.extend(new_letters)
# - - - - - - END OF CLASS PLAYER - - - - - - - - - - - -

# - BAG CLASS - - - - - - - - - - - -
class Bag:

  # - - CONSTRUCTOR - - - - -
  def __init__(self, dict):
    self.dict = dict

  # - - FUNCTIONS - - - - - - - - - - -
  # - - - Counts - 1 for a letter that got out of the bag - - - - -
  def remove_letter(self, letter):
    count = self.dict[letter]
    self.dict[letter] = count - 1
    if count == 0:
      self.dict.pop(letter)

  # - - - Checks if the bag is empty - - - - -
  def is_empty(self):
    if self.dict.keys() == 0:
      return True
    else:
      return False

  # - - - Removes a letter from the bag for 'num' times returns the letters needed - - - - -
  def draw_letters(self, num):
    needed_letters = []
    needed_letters = random.sample(list(self.dict.keys()), num)
    for letter in needed_letters:
      self.remove_letter(letter)
    return needed_letters
# - - - - - - END OF CLASS BAG - - - - - - - - - - - -

# - GAME CLASS - - - - - - - - - - - -
class Game:

  # - - CONSTRUCTOR - - - - - - - - - - -
  def __init__(self):
    self.active_rounds = 0
    self.active_player = 0
    self.players = []
    self.scores = players_score = {"0": 0,
                                   "1": 0}
    self.bag = Bag(letter_bag)

  # - - GETTERS - - - - - - - - - - - - -
  def get_active_player(self):
    return self.players[self.active_player]

  def get_bag(self):
    return self.bag
  # - - FUNCTIONS - - - - - - - - - - -

  # - - - Adds a player to the game - - - - -
  def add_player(self, player):
    self.players.append(player)

  # - - - Changes the players turn - - - - -
  def update_active_player(self):
    active_player = self.get_active_player()
    if active_player.value == 0:
      self.active_player = 1
    else: 
      self.active_player = 0

  # - - - Checking if a word is valid by letters - - - - -
  def check_letters(self, word, player): 
    upper_word = word.upper()
    error = 0
    wrong_letters = []
    letters = player.get_active_letters().copy()
    for letter in upper_word:
      if letter not in letters:
        wrong_letters.append(letter)
        error += 1
      else:
        letters.remove(letter) 

    if error >2:
      print("You don't have the letters: " + str(wrong_letters))
      return False

    if error == 0:
      player.set_active_letters(letters)
      return True

    if error == 1:
      if '*' in letters:
        letters.remove('*')
        player.set_active_letters(letters)
        return True
      else:
        print("You don't have the letters: " + str(wrong_letters))
        return False

    if error == 2:
      for i in range(2):
        if '*' in letters:
          letters.remove('*')
        else:
          print("You don't have the letters: " + str(wrong_letters))
          return False  

  def change_letter(self, player, bag):
    print("You have " + str(player.get_letter_changes()) + " changes left")
    print("Your letters are: " + str(player.get_active_letters()))
    letter = input("What letter would you like to change? ").upper()

    if letter in player.get_active_letters():
        player.get_active_letters().remove(letter)  # Remove the old letter
        new_letter = bag.draw_letters(1)[0]  # Draw a new letter
        player.get_active_letters().append(new_letter)  # Add the new letter
        print(f"Letter {letter} changed to {new_letter}")
    else:
        print("You don't have that letter.")
# - - - - - - END OF CLASS GAME - - - - - - - - - - - -

turn_timed_out = threading.Event()  # Event to track if time has expired

def turn_timeout():
  print("\n⏳ Time's up! Next player's turn.")
  turn_timed_out.set()  # Signal that the timer expired

def get_user_input():
  global word
  word = input("Enter a word: ").strip().lower()
  turn_timed_out.set()  # If the player enters a word, stop the timer

# * - * - * MAIN FUNCTIONALITY * - * - * - * - * - * - *

# INITIALIZING:
if __name__ == "__name__":
  game = Game()
  # PLAYER 1:  
  player1 = Player(input("~PLAYER 1~\nEnter your name: "), 0)
  player1.update_active_letters(game.get_bag())
  game.add_player(player1)
  # PLAYER 2:
  player2 = Player(input("~PLAYER 2~\nEnter your name: "), 1)
  player2.update_active_letters(game.get_bag())
  game.add_player(player2)

  # GAME LOOP:import threading
  while not game.get_bag().is_empty():
    turn_timed_out.clear()  # Reset timeout flag at the start of each turn

    print("You have 2 minutes to write a word.")
    timer = threading.Timer(120, turn_timeout)  # Change to 10 seconds for testing
    timer.start()

    active_player = game.get_active_player()
    print(f"{active_player.get_name()}, it's your turn!")
    print("Enter a word using the letters or enter 1 to change a letter:")
    print("Your letters:", active_player.get_active_letters())

    word = None
    start_time = time.time()

    # Non-blocking input loop
    while time.time() - start_time < 120:  # Give 10 seconds for input
        if turn_timed_out.is_set():
            break  # Exit input loop if time runs out

        if sys.stdin in select.select([sys.stdin], [], [], 1)[0]:
            word = input().strip().lower()
            break

    timer.cancel()  # Stop the timer

    if turn_timed_out.is_set():
        print("⏳ Time ran out! Skipping turn.")
        game.update_active_player()
        continue  # Skip to the next loop iteration

    if not word:
        continue  # If no word was entered, restart the turn

    if word == "1":
        game.change_letter(active_player, game.get_bag())
        active_player.set_letter_changes(active_player.get_letter_changes() - 1)
        print("Enter a word using the letters:", active_player.get_active_letters())
        word = input().lower()

    if twl.check(word) and game.check_letters(word, active_player):
        print("✅ Valid word!")
        for letter in word:
            game.scores[str(active_player.get_value())] += letter_value[letter.upper()]
        print(active_player.get_name(), "has", game.scores[str(active_player.get_value())], "points")

        active_player.update_active_letters(game.get_bag())  # Update letters
    else:
        print("❌ Invalid word, try again!")

    game.update_active_player()  # Move to next player
