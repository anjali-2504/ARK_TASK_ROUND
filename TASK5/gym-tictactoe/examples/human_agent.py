#!/usr/bin/env python
import sys
import click
import random
from gym_tictactoe.env import TicTacToeEnv, agent_by_mark, check_game_status,\
    after_action_state, tomark, next_mark

class BaseAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, state, ava_actions):
        for action in ava_actions:
            nstate = after_action_state(state, action)
            gstatus = check_game_status(nstate[0])
            if gstatus > 0:
                if tomark(gstatus) == self.mark:
                    return action
        return random.choice(ava_actions)

class HumanAgent(object):
    def __init__(self, mark):
        self.mark = mark

    def act(self, ava_actions):
        while True:
            uloc = input("Enter location[1-9], q for quit: ")
            if uloc.lower() == 'q':
                return None
            try:
                action = int(uloc) - 1
                if action not in ava_actions:
                    raise ValueError()
            except ValueError:
                print("Illegal location: '{}'".format(uloc))
            else:
                break

        return action


@click.command(help="Play human agent.")
@click.option('-n', '--show-number', is_flag=True, default=False,
              show_default=True, help="Show location number in the board.")
def play(show_number):
    start_mark = 'X'
    env = TicTacToeEnv(show_number=show_number)
    agents = [BaseAgent('O'),
              HumanAgent('X')]
    episode = 0
    while True:
        env.set_start_mark(start_mark)
        state = env.reset()
        _, mark = state

        done = False
        env.render()
        agent = agent_by_mark(agents, mark)

        while not done:
            agent = agent_by_mark(agents, mark)
            env.show_turn(True, mark)
            action =None
            
            
            if agent.mark=='O':
                action = env.available_actions()
            else:
                ava_actions = env.available_actions_h()
                action = agent.act(ava_actions)
            if action is None:
                sys.exit()
            print("action  {}".format(action))
            state, reward, done, info = env.step(action)

            print('')
            env.render()
            if done:
                env.show_result(True, mark, reward)
                break
            else:
                _, mark = state
        episode += 1


if __name__ == '__main__':
    play()
