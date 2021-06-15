import sys
sys.path.append("/home/anjali/winterworkshop/Q_learn_github2/tictactoe.py")
from agent import Agent
from tictactoe import TicTacToe

def play(agent):
    game = TicTacToe()
    while True:
        action = agent.qlearner.get_best_action(game.get_state())
        winner = game.play(*action)
        if winner:
            print("**** you lost ****")
            return
        if game.is_ended():
            print("**** draw ****")
            return
        x, y ,z= input("input x and y and z: ").split()
        winner = game.play(int(x), int(y),int(z))
        if winner:
            print("**** you won ****")
            return
        if game.is_ended():
            print("**** draw ****")
            return

q_agent = Agent()
print("learning...")
q_agent.learn()
print("done")

while True:
    print("\nlet's play\n")
    play(q_agent)