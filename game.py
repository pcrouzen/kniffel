import dice
import scorers

Scorers = (
    [scorers.OnlyMatchingScorer(i) for i in range(1,6)] +
    [scorers.AtLeastNMatchingScorer(i) for i in [3,4]] +
    [scorers.FullHouseScorer()])

def GetRerollIndices(d):
  print "Pick dice to reroll or [Enter]"
  print "0 1 2 3 4"
  print " ".join(["{0}".format(p) for p in d.get_dice()])
  return map(int, raw_input().split())

def Turn(available_scorers):
  d = dice.DiceTurn(5)
  d.roll()
  num_rerolls = 0
  while num_rerolls < 2:
    indices_to_reroll = GetRerollIndices(d)
    if len(indices_to_reroll) == 0:
      break
    d.reroll(indices_to_reroll)
    num_rerolls = num_rerolls + 1
  print "Final roll:"
  print " ".join(["{0}".format(p) for p in d.get_dice()])
    
  


Turn([])
