from itertools import groupby

class Scorer:
  def __init__(self):
    self.name = "Scorer"

  def ComputeScore(self, dice):
    return 0

class OnlyMatchingScorer(Scorer):
  def __init__(self, pips):
    self.pips = pips
    self.name = "Only %ds" % self.pips

  def ComputeScore(self, dice):
    return sum([d for d in dice if d == self.pips])

class AtLeastNMatchingScorer(Scorer):
  def __init__(self, n, fixed_score=None, name=None):
    self.n = n
    self.fixed_score = fixed_score
    if name:
      self.name = name
    else:
      self.name = "%d equal" % self.n

  def ComputeScore(self, dice):
    sorted_dice = sorted(dice)
    for d,l in groupby(sorted_dice):
      if len(list(l)) >= self.n:
        return self.fixed_score or sum(dice)
    return 0
      
class FullHouseScorer(Scorer):
  def __init__(self):
    self.name = "Full House"

  def ComputeScore(self, dice):
    sorted_dice = sorted(dice)
    group_lengths = sorted([len(list(l)) for d,l in groupby(sorted_dice)])
    if group_lengths == [2,3]:
      return 25
    else:
      return 0     

class StreetScorer(Scorer):
  def __init__(self, length, name, score):
    if length == 4:
      self.name = "Short street"
    elif length == 5:
      self.name = "Long street"
    else:
      self.name = "Street %d" % length
    self.length = length
    self.score = score

  def ComputeScore(self, dice):
    found_length = 0
    for i in range(1,7):
      if i in dice:
        found_length += 1
        if found_length == self.length:
          return self.score
      else:
        found_length = 0

    return 0
