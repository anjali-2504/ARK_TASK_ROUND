from collections import defaultdict
import pickle

class Q:
    def __init__(self, alpha=0.5, discount=0.5,values= defaultdict(lambda: defaultdict(lambda: 0.0))):
        self.alpha = alpha
        self.discount = discount
        self.values =values

    def update(self, state, action, next_state, reward):
        value = self.values[state][action]
        v = list(self.values[next_state].values())
        next_q = max(v) if v else 0
        value = value + self.alpha * (reward + self.discount * next_q - value)
        self.values[state][action] = value

    def get_best_action(self, state):
        keys = list(self.values[state].keys())
        if not keys:
            return None
        return max(keys, key=lambda x: self.values[state][x])

  
