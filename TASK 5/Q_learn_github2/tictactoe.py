class TicTacToe:
    def __init__(self, render=True):
        self.board = [[[0, 0, 0],[0, 0, 0],[0, 0, 0]] for _ in range(3)]
        self.player = 1
        self.repr = {0: ".", 1: "x", -1: "o"}
        self.render = render

    def _get_winner(self):
        # check horizontal
        for i in range(3):
            for j in range(3):
                if abs(sum(self.board[i][j])) == 3:
                    return self.board[i][j][0]

        # check vertical
        for k in range(3):
            for i in range(3):
                if abs(sum(self.board[k][j][i] for j in range(3))) == 3:
                    return self.board[k][0][i]
  
        for i in range(3):
            for j in range(3):
                if abs(sum(self.board[k][j][i] for k in range(3))) ==3:
                    return self.board[0][j][i]          

        # check diagonal
        for k in range(3):
            if abs(sum(self.board[k][i][i] for i in range(3))) == 3:
                return self.board[k][0][0]
            if abs(sum(self.board[k][i][2 - i] for i in range(3))) == 3:
                return self.board[k][0][2]


        for i in range(3):
            if abs(sum(self.board[k][k][i] for k in range(3))) == 3:
                return self.board[0][0][i]
            if abs(sum(self.board[2-k][k][i] for k in range(3))) == 3:
                return self.board[0][2][i]       
        
        for i in range(3):
            if abs(sum(self.board[k][i][k] for k in range(3))) == 3:
                return self.board[0][i][0]
            if abs(sum(self.board[2-k][i][k] for k in range(3))) == 3:
                return self.board[0][i][2]   

        
        if abs(sum(self.board[i][i][i] for i in range(3)))==3:
            return self.board[0][0][0]  
        if abs(sum(self.board[i][2-i][2-i] for i in range(3)))==3:
            return self.board[0][2][2]
        if abs(sum(self.board[i][2-i][i]for i in range(3)))==3:
            return self.board[0][2][0]
        if abs(sum(self.board[i][i][2-i] for i in range(3)))==3:
            return self.board[0][0][2]         


                

        return None

    def get_state(self):
        return str(self.board)

    def get_valid_actions(self):
        actions = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if self.board[i][j][k] == 0:
                        actions.append((i,j,k))
        return actions

    def is_ended(self):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    if self.board[i][j][k] == 0:
                        return False
        return True

    def _print(self):
        '''for row in self.board:
            for item in row:
                for x in item:
                    print(self.repr[x], end="\t")
                print("\n")    
            print("\n")
            print("-----------------\n")
        print("-----------------------------------\n") '''

        for i in range(3):
            for k in range(3):
                for j in range(3):
                    print(self.repr[self.board[k][i][j]], end=' ')
                    if(k<2):    
                        print(" | ", end='\t')
                    else:
                        print(end='\n')
                        print("--------------------------------------")       

    def play(self, x, y,z):
        if self.board[x][y][z] != 0:
            return None

        self.board[x][y][z] = self.player
        if self.render:
            self._print()
        winner = self._get_winner()
        if winner:
            return winner
        self.player *= -1
        return None