import random

def RollDice(num_dice):
  return [random.randint(1,6) for x in range(num_dice)]

class DiceTurn:
  def __init__(self, num_dice):
    self.num_dice = num_dice
    self.dice = []

  def roll(self):
    self.dice = RollDice(self.num_dice)
    return self.dice

  def reroll(self, indices):
    for i in indices:
      self.dice[i] = random.randint(1,6)
    return self.dice

  def get_dice(self):
    return self.dice


  
