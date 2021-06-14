import cv2 as cv2
import numpy as np
import colorsys
img_ = cv2.imread("maze_lv3.png",1)
img=img_.copy()

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        #for k in range(3):
        if(img[i][j][0]!=230):
            img[i][j][0]=0
            img[i][j][1]=0
            img[i][j][2]=0
cv2.namedWindow("IMAGE")

h, w = img.shape[:2]
class Node():

    def __init__(self, state, parent):
        self.state = state
        self.parent = parent

class StackFrontier():

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("The frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)


class Maze():

    def __init__(self, start,end):
        global h,w
        self.height = h
        self.width = w
        self.start=start
        self.goal=end


    def neighbors(self, state):
        row, col = state
        candidates = [
            (row - 12, col),
            (row + 12, col),
            (row, col-12),
             (row, col+12)
        ]
        result = []
        for (r, c) in candidates:
            if r==row-12:
                if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img1[c][r+6][0] == 0 and img1[c][r+6][1] == 0 and img1[c][r+6][2] == 0):
                    result.append( (r, c))

            if r==row+12:
                if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img1[c][r-6][0] == 0 and img1[c][r-6][1] == 0 and img1[c][r-6][2] == 0):
                    result.append( (r, c))   

            if c==col-12:
                if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img1[c+6][r][0] == 0 and img1[c+6][r][1] == 0 and img1[c+6][r][2] == 0):
                    result.append( (r, c))

            if c==col+12:
                if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img1[c-6][r][0] == 0 and img1[c-6][r][1] == 0 and img1[c-6][r][2] == 0):
                    result.append( (r, c))        

        return result


    def DFS(self):

        self.num_explored = 0

        start = Node(state=self.start, parent=None)
        frontier = StackFrontier()
        frontier.add(start)

        self.explored = set()

        while True:
            cv2.imshow("IMAGE", img)
            cv2.waitKey(1)

            node = frontier.remove()
            self.num_explored += 1

            if node.state[0] == self.goal[0] and node.state[1]==self.goal[1]:
    
                cells = []
                print(self.num_explored)
                

                while node.parent is not None:
                   
                    cells.append(node.state)
                    node = node.parent
             
                cells.reverse()
             #   self.solution = (cells)
                for (x,y) in cells:
                    for i in range(2):
                        for j in range(2):
                            img[y-i][x-j]=[0,255,0]
                            img[y+i][x+j]=[0,255,0]
                return
            self.explored.add(node.state)

            for  state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node)
                   # print(state)
                
                    for i in range(2):
                        for j in range(2):
                            img[state[1]-i][state[0]-j]=[0,0,255]
                            img[state[1]+i][state[0]+j]=[0,0,255]

                    frontier.add(child)
        
maze=Maze((60,156),(420,144))
img1=img.copy()
maze.DFS()
cv2.imshow("IMAGE", img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
