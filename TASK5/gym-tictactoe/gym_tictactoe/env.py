import logging

import gym
from gym import spaces
import math
import cv2 as cv2
import numpy as np

cv2.namedWindow("tic-tac_toe")

CODE_MARK_MAP = {0: ' ', 1: 'O', 2: 'X'}
NUM_LOC = 9
O_REWARD = 1
X_REWARD = -1
NO_REWARD = 0

LEFT_PAD = '  '
LOG_FMT = logging.Formatter('%(levelname)s '
                            '[%(filename)s:%(lineno)d] %(message)s',
                            '%Y-%m-%d %H:%M:%S')


def tomark(code):
    return CODE_MARK_MAP[code]


def tocode(mark):
    return 1 if mark == 'O' else 2


def next_mark(mark):
    return 'X' if mark == 'O' else 'O'


def agent_by_mark(agents, mark):
    for agent in agents:
        if agent.mark == mark:
            return agent


def after_action_state(state, action):
    """Execute an action and returns resulted state.

    Args:
        state (tuple): Board status + mark
        action (int): Action to run

    Returns:
        tuple: New state
    """

    board, mark = state
    nboard = list(board[:])
    nboard[action] = tocode(mark)
    nboard = tuple(nboard)
    return nboard, next_mark(mark)
# Python3 program to find the next optimal move for a player
player, opponent = 'X', 'O'

img_1 = np.zeros([513,513,1],dtype=np.uint8)
img_1.fill(255) 
for i in range(151,181):
    for j in range(img_1.shape[1]):
        img_1[i][j]=0
for j in range(151,181):
    for i in range(img_1.shape[0]):
        img_1[i][j]=0 

for i in range(332,362):
    for j in range(img_1.shape[1]):
        img_1[i][j]=0               

for j in range(332,362):
    for i in range(img_1.shape[0]):
        img_1[i][j]=0 
        

def minimax(board, depth, isMax):
    score = check_game_status(board)

    if (score == 1 ):
        return O_REWARD

    if (score == 2):
        return X_REWARD

    if (score==0):
        return 0   ###

    if (isMax):
        best = -math.inf

        for j in range(len(board)):
            if ( board[j]==0):
                board[j] =1
                best = max(best, minimax(board,
                                             depth + 1,
                                             not isMax)-1)
                board[j] = 0
        return best
    else:
        best = math.inf

        for j in range(len(board)):
            if (board[j]==0):

                board[j] =2
                best = min(best, minimax(board, depth + 1, not isMax)+1)
                board[j] = 0
        return best


def check_game_status(board):
    """Return game status by current board status.

    Args:
        board (list): Current board state

    Returns:
        int:
            -1: game in progress
            0: draw game,
            1 or 2 for finished game(winner mark code).
    """
    for t in [1, 2]:
        for j in range(0, 9, 3):
            if [t] * 3 == [board[i] for i in range(j, j+3)]:
                return t
        for j in range(0, 3):
            if board[j] == t and board[j+3] == t and board[j+6] == t:
                return t
        if board[0] == t and board[4] == t and board[8] == t:
            return t
        if board[2] == t and board[4] == t and board[6] == t:
            return t

    for i in range(9):
        #print(board[i])
        if board[i]==0:
            return -1

    # draw game
    return 0


class TicTacToeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, alpha=0.02, show_number=False):
        self.action_space = spaces.Discrete(NUM_LOC)
        self.observation_space = spaces.Discrete(NUM_LOC)
        self.alpha = alpha
        self.set_start_mark('X')
        self.show_number = show_number
        self.seed()
        self.reset()

    def set_start_mark(self, mark):
        self.start_mark = mark

    def reset(self):
        self.board = [0] * NUM_LOC
        self.mark = self.start_mark
        self.done = False
        return self._get_obs()

    def step(self, action):
        """Step environment by action.

        Args:
            action (int): Location

        Returns:
            list: Obeservation
            int: Reward
            bool: Done
            dict: Additional information
        """
        assert self.action_space.contains(action)

        loc = action
        if self.done:
            return self._get_obs(), 0, True, None

        reward = NO_REWARD
        # place
        self.board[loc] = tocode(self.mark)
        
        status = check_game_status(self.board)
        logging.debug("check_game_status board {} mark '{}'"
                      " status {}".format(self.board, self.mark, status))
        print(status)              
        if status >= 0:
            self.done = True
            if status in [1, 2]:
                # always called by self
                reward = O_REWARD if self.mark == 'O' else X_REWARD
    
        # switch turn
        self.mark = next_mark(self.mark)
        return self._get_obs(), reward, self.done, None

    def _get_obs(self):
        return tuple(self.board), self.mark

    def render(self, mode='human', close=False):
        if close:
            return
        if mode == 'human':
            self._show_board(print)  # NOQA
            print('')
        else:
            self._show_board(logging.info)
            logging.info('')

    def show_episode(self, human, episode):
        self._show_episode(print if human else logging.warning, episode)

    def _show_episode(self, showfn, episode):
        showfn("==== Episode {} ====".format(episode))

    def _show_board(self, showfn):
        """Draw tictactoe board."""
        for j in range(0, 9, 3):
            
            def mark(i):
                if(self.board[i]==1 or self.board[i]==2 or self.board[i]==0):
                    return tomark(self.board[i])
    
            print(LEFT_PAD + '|'.join([mark(i) for i in range(j, j+3)]))
            if j < 6:
                print(LEFT_PAD + '-----')


        ''' cv2.imshow('tic-tac-toe', img_1)   
        cv2.waitKey(0)
        cv2.destroyAllWindows() '''


    def show_turn(self, human, mark):
        self._show_turn(print if human else logging.info, mark)

    def _show_turn(self, showfn, mark):
        showfn("{}'s turn.".format(mark))

    def show_result(self, human, mark, reward):
        self._show_result(print if human else logging.info, mark, reward)

    def _show_result(self, showfn, mark, reward):
        status = check_game_status(self.board)
        assert status >= 0
        if status == 0:
            showfn("==== Finished: Draw ====")
        else:
            msg = "Winner is '{}'!".format(tomark(status))
            showfn("==== Finished: {} ====".format(msg))
        showfn('')

    def available_actions(self):
        best_score= - math.inf
        best_move = -4
        for i in range(len(self.board)):
            if self.board[i]==0:
                count=0
                self.board[i]=1
      # new_board=self.board.copy()
                score=minimax(self.board,0,True)
                self.board[i]=0

                if(score>best_score):
                    best_score=score
                    best_move= i
        return (best_move)
       # return [i for i, c in enumerate(self.board) if c == 0]
    def available_actions_h(self):   
        return [i for i, c in enumerate(self.board) if c == 0 ]

    

def set_log_level_by(verbosity):
    """Set log level by verbosity level.

    verbosity vs log level:

        0 -> logging.ERROR
        1 -> logging.WARNING
        2 -> logging.INFO
        3 -> logging.DEBUG

    Args:
        verbosity (int): Verbosity level given by CLI option.

    Returns:
        (int): Matching log level.
    """
    if verbosity == 0:
        level = 40
    elif verbosity == 1:
        level = 30
    elif verbosity == 2:
        level = 20
    elif verbosity >= 3:
        level = 10

    logger = logging.getLogger()
    logger.setLevel(level)
    if len(logger.handlers):
        handler = logger.handlers[0]
    else:
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    handler.setLevel(level)
    handler.setFormatter(LOG_FMT)
    return level
