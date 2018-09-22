import dice
import scorers
import ui

STATE_START = 1
STATE_REROLLING = 2

Scorers = (
    [scorers.OnlyMatchingScorer(i) for i in range(1,7)] +
    [scorers.AtLeastNMatchingScorer(i) for i in [3,4]] +
    [scorers.FullHouseScorer()] +
    [scorers.StreetScorer(i, name, score) for 
         i,name,score in [(4, "Short street", 30), (5, "Long street", 40)]] +
    [scorers.AtLeastNMatchingScorer(5, fixed_score=50, name="Yahtzee!")] +
    [scorers.AtLeastNMatchingScorer(1, name="Chance")]
)


class GameController:
  def __init__(self):
    self.scorers = Scorers
    num_scorers = len(self.scorers)
    self.scores = [None for i in range(num_scorers)]
    self.num_scorers_remaining = num_scorers
    scorer_names_and_fns = zip([scorer.name for scorer in self.scorers], 
                               [lambda i=i: self.on_scorer(i) for i in range(num_scorers)])
    self.app = ui.GameApplication(self.on_roll, self.on_reroll, scorer_names_and_fns)
    self.new_turn_or_finish()

  def new_turn_or_finish(self):
    self.app.reset_reroll()
    self.app.clear_dice()
    if (self.num_scorers_remaining == 0):
      self.finish_game()
    self.state = STATE_START
    self.num_rerolls_available = 2
    self.current_dice = dice.DiceTurn(5)
    self.app.disable_buttons_except_roll()

  def finish_game(self):
    self.app.disable_all_buttons_except_quit()
    self.app.write_total_score(sum(self.scores))

  def on_roll(self):
    assert (self.state == STATE_START)
    self.current_dice.roll()
    self.app.redraw_dice(self.current_dice.get_dice())
    self.state = STATE_REROLLING
    self.app.enable_buttons_except_roll([i for i in range(len(self.scores)) if self.scores[i] == None])

  def on_reroll(self):
    assert (self.state == STATE_REROLLING)
    assert (self.num_rerolls_available > 0)
    self.current_dice.reroll(self.app.get_reroll_dice())
    self.app.redraw_dice(self.current_dice.get_dice())
    self.num_rerolls_available = self.num_rerolls_available - 1
    if self.num_rerolls_available == 0:
      self.app.disable_reroll_and_hold_buttons()

  def on_scorer(self, i):
    assert (self.state == STATE_REROLLING)
    assert (self.scores[i] == None)
    self.scores[i] = self.scorers[i].ComputeScore(self.current_dice.get_dice())
    self.app.write_score(i, self.scores[i])
    self.num_scorers_remaining -= 1

    self.new_turn_or_finish()


gc = GameController()
gc.app.master.title('Kniffel')
gc.app.mainloop() 
