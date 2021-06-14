# Make a copy of this file
# and Add a class called AI Agent 
import pickle
import sys
import json
from gym_tictactoe.envs.agents import Agent
from gym_tictactoe.envs.tictactoe_env import TicTacToeEnv,  agent_by_mark

def play(agent):
    env = TicTacToeEnv()

    episode = 0
    done = False
    while not done:
        action = agent.qlearner.get_best_action(env.get_state())
        print(action)
        if action is None:
            sys.exit()
        state, reward, done, info = env.step(*action)
        print()
        env._print()
        if done:
            env.show_result()
            break
        x, y ,z= input("input x and y and z: ").split()
        state, reward, done, info = env.step(int(x), int(y),int(z))  
        if done:
            env.show_result()
            break
    episode += 1

q_agent = Agent()
print("learning...")
q_agent.learn()
print("done")
Q_VAL=q_agent.q_VAL



f = open("file.pkl","wb")
pickle.dump(dict,f)
f.close()    
#print(Q_VAL)
#pickle.dump(Q_VAL, open("Q_value.txt", "wb"))

if __name__ == '__main__':
    play(q_agent)