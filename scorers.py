from itertools import groupby

class Scorer:
  def ComputeScore(self, dice):
    return 0

class OnlyMatchingScorer(Scorer):
  def __init__(self, pips):
    self.pips = pips

  def ComputeScore(self, dice):
    return sum([d for d in dice if d == self.pips])

class AtLeastNMatchingScorer(Scorer):
  def __init__(self, n):
    self.n = n

  def ComputeScore(self, dice):
    sorted_dice = sorted(dice)
    for d,l in groupby(sorted_dice):
      if len(list(l)) >= self.n:
        return sum(dice)
    return 0
      
class FullHouseScorer(Scorer):
  def ComputeScore(self, dice):
    sorted_dice = sorted(dice)
    group_lengths = sorted([len(l) for d,l in groupby(sorted_dice)])
    if group_lengths == [2,3]:
      return 25
    else:
      return 0     
