import Tkinter as tk

class DiceButton():
  def __init__(self, parent, number, state=tk.NORMAL):
    self.number = number
    self.parent = parent
    self.frame = tk.Frame(parent)
    self.frame.grid(row=0, column=self.number)
    self.diceCanvas = tk.Canvas(
        self.frame, width=80, height=80)
    self.diceCanvas.create_rectangle(5, 5, 76, 76, tag='rect')
    self.diceCanvas.grid()
    self.button = tk.Button(self.frame, text='Keep', state=state, command=self.pushed)
    self.button.grid()

    self.marked = False

  def set_state(self, state):
    self.button.config(state=state)

  def reset(self):
    self.marked = False
    self.drawMarked()

  def pushed(self):
    print 'Pushed dice %d' % self.number
    self.marked = not self.marked
    self.drawMarked()

  def drawMarked(self):
    if self.marked:
      self.diceCanvas.itemconfigure('rect', fill='cyan')
    else:
      self.diceCanvas.itemconfigure('rect', fill='')

  def clear(self):
    self.diceCanvas.delete('pip')

  def draw_pips(self, num_pips):
    self.clear()
    if num_pips == 1:
      self.diceCanvas.create_oval(35,35,46,46,tags=['pip'])
    if num_pips == 2:
      self.diceCanvas.create_oval(10,10,21,21,tags=['pip'])
      self.diceCanvas.create_oval(60,60,71,71,tags=['pip'])
    if num_pips == 3:
      self.diceCanvas.create_oval(10,10,21,21,tags=['pip'])
      self.diceCanvas.create_oval(35,35,46,46,tags=['pip'])
      self.diceCanvas.create_oval(60,60,71,71,tags=['pip'])
    if num_pips == 4:
      self.diceCanvas.create_oval(10,10,21,21,tags=['pip'])
      self.diceCanvas.create_oval(10,60,21,71,tags=['pip'])
      self.diceCanvas.create_oval(60,60,71,71,tags=['pip'])
      self.diceCanvas.create_oval(60,10,71,21,tags=['pip'])
    if num_pips == 5:
      self.diceCanvas.create_oval(10,10,21,21,tags=['pip'])
      self.diceCanvas.create_oval(10,60,21,71,tags=['pip'])
      self.diceCanvas.create_oval(60,60,71,71,tags=['pip'])
      self.diceCanvas.create_oval(60,10,71,21,tags=['pip'])
      self.diceCanvas.create_oval(35,35,46,46,tags=['pip'])
    if num_pips == 6:
      self.diceCanvas.create_oval(10,10,21,21,tags=['pip'])
      self.diceCanvas.create_oval(10,35,21,46,tags=['pip'])
      self.diceCanvas.create_oval(10,60,21,71,tags=['pip'])
      self.diceCanvas.create_oval(60,60,71,71,tags=['pip'])
      self.diceCanvas.create_oval(60,35,71,46,tags=['pip'])
      self.diceCanvas.create_oval(60,10,71,21,tags=['pip'])

class GameApplication(tk.Frame):
    def __init__(self, on_roll, on_reroll, names_and_on_scorer_fns):
        tk.Frame.__init__(self, None)
        self.on_roll = on_roll
        self.on_reroll = on_reroll
        self.names_and_on_scorer_fns = names_and_on_scorer_fns
        self.grid()
        self.createWidgets()

    def createWidgets(self):
        num_scorers = len(self.names_and_on_scorer_fns)
        self.scorerFrame = tk.Frame(self, width=600, height=num_scorers*100)
        self.scorerFrame.grid()
        i = 0
        self.scoreButtons = []
        self.scoreStrings = []
        for scorer_name, on_scorer_fn in self.names_and_on_scorer_fns:
          scoreButton = tk.Button(self.scorerFrame, text=scorer_name, command=on_scorer_fn)
          scoreButton.grid(row=i, column=0)
          self.scoreButtons.append(scoreButton)

          scoreString = tk.StringVar()
          scoreTextBox = tk.Entry(
              self.scorerFrame, width=3, textvariable=scoreString, state=tk.DISABLED)
          scoreTextBox.grid(row=i, column=1)
          self.scoreStrings.append(scoreString)
          
          i += 1

        totalScoreText = tk.Label(self.scorerFrame, text="Total score")
        totalScoreText.grid(row=i, column=0)

        self.totalScoreString = tk.StringVar()
        totalScoreBox = tk.Entry(
            self.scorerFrame, width=3, textvariable=self.totalScoreString,
            state=tk.DISABLED)
        totalScoreBox.grid(row=i, column=1)

        self.diceFrame = tk.Frame(self, width=600, height=100)
        self.diceFrame.grid()

        self.diceButtons = []
        for i in range(5):
            self.diceButtons.append(DiceButton(self.diceFrame, i, state=tk.DISABLED))

        self.rollButton = tk.Button(self, text='Roll', command=self.on_roll)
        self.rollButton.grid()

        self.rerollButton = tk.Button(
            self, text='Reroll', state=tk.DISABLED, command=self.on_reroll)
        self.rerollButton.grid()

        self.quitButton = tk.Button(self, text='Quit',
            command=self.quit)
        self.quitButton.grid()

    def redraw_dice(self, dice):
      assert (len(dice) == 5)
      for i, pips in zip(range(5), dice):
        self.diceButtons[i].draw_pips(pips)

    def enable_buttons_except_roll(self, enabled_scorers):
      self.rollButton.config(state = tk.DISABLED)
      self.rerollButton.config(state = tk.NORMAL)
      for i, scoreButton in zip(range(len(self.scoreButtons)), self.scoreButtons):
        if i in enabled_scorers:
          scoreButton.config(state = tk.NORMAL)
      for diceButton in self.diceButtons:
        diceButton.set_state(tk.NORMAL)

    def disable_buttons_except_roll(self):
      self.rollButton.config(state = tk.NORMAL)
      self.rerollButton.config(state = tk.DISABLED)
      for scoreButton in self.scoreButtons:
        scoreButton.config(state = tk.DISABLED)
      for diceButton in self.diceButtons:
        diceButton.set_state(tk.DISABLED)

    def disable_all_buttons_except_quit(self):
      self.disable_buttons_except_roll()
      self.rollButton.config(state = tk.DISABLED)

    def _write_score(self, stringVar, score):
      stringVar.set("%d" % score)
    
    def write_score(self, i, score):
      self._write_score(self.scoreStrings[i], score)

    def write_total_score(self, score):
      self._write_score(self.totalScoreString, score)

    def clear_dice(self):
      for diceButton in self.diceButtons:
        diceButton.clear()

    def get_reroll_dice(self):
      return [i for i, diceButton in 
          zip(range(len(self.diceButtons)), self.diceButtons) if not diceButton.marked]

    def reset_reroll(self):
      for diceButton in self.diceButtons:
        diceButton.reset()

    def disable_reroll_and_hold_buttons(self):
      self.rerollButton.config(state=tk.DISABLED)
      for diceButton in self.diceButtons:
        diceButton.set_state(tk.DISABLED)
