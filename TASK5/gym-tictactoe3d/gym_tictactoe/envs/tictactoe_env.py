import gym
from gym import error, spaces, utils
from gym.utils import seeding
import copy

def agent_by_mark(agents, mark):
  for agent in agents:
        if agent.mark == mark:
            return agent


class TicTacToeEnv(gym.Env):

  metadata = {'render.modes': ['bcr','compact','full']}
  _EMPTY = '-'
  _X = 'x'
  _O = 'o'
  _PLAYERS = [_EMPTY, _X, _O]
  _PLAYERS_COUNT = 2

  _MAX_ROUND = 3 * 3 * 3

  def __init__(self,render=True, ):
    self._round = 0
    self._result = None
    self._world = [[[0, 0, 0],[0, 0, 0],[0, 0, 0]] for _ in range(3)]
    self._done = False
    self.render=render
    self.player = 1

  def step(self, b, c, r):

      self._round += 1
     # print(b, c, r)

      if self._world[b][c][r] != 0:
        if self.is_ended():
          self._done = True
        info = {'round': self._round}
        return str(self._world), -100 if self._done else 0, self._done, info

      self._world[b][c][r] = self.player
      self.player *= -1
      self._result = self._get_winner()
      self._done = (True if self._result else False)
      info = {'round': self._round}
      return str(self._world), 100 if self._done else 0, self._done, info

  def get_as_char(self, b, c, r, winning_seq=None):
    val = self._world[b][c][r]
    ret = TicTacToeEnv._PLAYERS[val]

    if winning_seq and (b,c,r) in winning_seq:
      return ret.upper()
    else:
      return ret

  def reset(self):
    self._round = 0
    self._world = [[[0, 0, 0],[0, 0, 0],[0, 0, 0]] for _ in range(3)]
    self._done = False
    return self._world

  def _print(self, mode='compact', close=False):
    for r in range(3):
      for b in range(3):
        for c in range(3):
            print(self.get_as_char(b, c, r), end=' ')
        print('   ', end='')
      print()

  def _get_winner(self):
    for i in range(3):
      for j in range(3):
        if abs(sum(self._world[i][j])) == 3:
          return self._world[i][j][0]
    for k in range(3):
      for i in range(3):
        if abs(sum(self._world[k][j][i] for j in range(3))) == 3:
          return self._world[k][0][i]

    for i in range(3):
      for j in range(3):
          if abs(sum(self._world[k][j][i] for k in range(3))) == 3:
                    return self._world[0][j][i]
    for k in range(3):
      if abs(sum(self._world[k][i][i] for i in range(3))) == 3:
        return self._world[k][0][0]
      if abs(sum(self._world[k][i][2 - i] for i in range(3))) == 3:
        return self._world[k][0][2]

    for i in range(3):
      if abs(sum(self._world[k][k][i] for k in range(3))) == 3:
        return self._world[0][0][i]
      if abs(sum(self._world[2-k][k][i] for k in range(3))) == 3:
        return self._world[0][2][i]

    for i in range(3):
      if abs(sum(self._world[k][i][k] for k in range(3))) == 3:
        return self._world[0][i][0]
      if abs(sum(self._world[2-k][i][k] for k in range(3))) == 3:
        return self._world[0][i][2]

    if abs(sum(self._world[i][i][i] for i in range(3))) == 3:
      return self._world[0][0][0]
    if abs(sum(self._world[i][2-i][2-i] for i in range(3))) == 3:
      return self._world[0][2][2]
    if abs(sum(self._world[i][2-i][i]for i in range(3))) == 3:
      return self._world[0][2][0]
    if abs(sum(self._world[i][i][2-i] for i in range(3))) == 3:
      return self._world[0][0][2]

    return None


  def get_state(self):
    return str(self._world)

  def show_turn(self):
    return (self._round % TicTacToeEnv._PLAYERS_COUNT) + 1

  def show_result(self):
      msg = "Winner is '{}'!".format(self._result)
      print("==== Finished: {} ====".format(msg))
      return self._result
  
  def available_actions(self):
    available = []
    for i in range(3):
      for j in range(3):
        for k in range(3):
          if self._world[i][j][k] == 0:
            available.append((i, j, k))
    return available

  def play(self, x, y,z):
    if self._world[x][y][z] != 0:
      return None

    self._world[x][y][z] = self.player
    if self.render:
      self._print()
    winner = self._get_winner()
    if winner:
      return winner
    self.player *= -1
    return None  


  def is_ended(self):
    for i in range(3):
      for j in range(3):
          for k in range(3):
            if self._world[i][j][k] == 0:
              return False
    self._done=True          
    return True      
