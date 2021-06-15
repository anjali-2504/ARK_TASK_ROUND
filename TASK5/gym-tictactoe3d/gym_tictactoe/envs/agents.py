import random
from gym_tictactoe.envs.Q import Q
from gym_tictactoe.envs.tictactoe_env import TicTacToeEnv, agent_by_mark

class Agent:
    def __init__(self,q_VAl=None):
        self.eps = 1.0
        self.qlearner = Q()
        self.q_VAL=q_VAl

    def _get_action(self, state, valid_actions):
        if random.random() < self.eps:
            return random.choice(valid_actions)
        best = self.qlearner.get_best_action(state)
        if best is None:
            return random.choice(valid_actions)
        return best

    def _learn_one_game(self):
        game = TicTacToeEnv(render=False)
        game.reset()
        while True:
            state = game.get_state()
            action= self._get_action(state, game.available_actions())
            state_NEW, reward, done, info = game.step(*action)

            if done or game.is_ended():
                self.qlearner.update(state, action, game.get_state(), 100)
                break

            state_NEW2, reward, done, info= game.step(*random.choice(game.available_actions()))
            if done or game.is_ended():
                self.qlearner.update(state, action,  game.get_state(), -100)
                break
            self.qlearner.update(state, action, game.get_state(), 0)

    def learn(self, n=20000):
        for _ in range(n):
            self._learn_one_game()
            self.eps -= 0.0001
        self.q_VAL=self.qlearner.values 
