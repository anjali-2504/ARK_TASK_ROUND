import cv2
import numpy as np
import math
import os 
import time
import random
array_x=[]
array_y=[]
def array_form():
    for i in range(12,445,12):
        array_x.append(i)
    for j in range(12,157,12):
        array_y.append(j)     
class RRTMap:
    def __init__(self, start, goal,img):
        self.start = start
        self.goal = goal
        self.map=img
      
    def drawPath(self, path):
        for node in path:
            for i in range(2):
                    for j in range(2):
                        self.map[node[1]-i][node[0]-j]=[0,255,0]
                        self.map[node[1]+i][node[0]+j]=[0,255,0]


obstacles = []
class RRTGraph:
    def __init__(self, start, goal, img):
        (x, y) = start
        self.start = start
        self.goal = goal
        self.goalFlag = False
        self.x = []
        self.y = []
        self.parent = []
       # self.dist_startnode=[]
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
     #  self.dist_startnode.append(0)
        self.goalstate = None
        self.path = []
        self.map=img
    def add_node(self, n, x, y):
        self.x.insert(n,x)
        self.y.append(y)
        
    def remove_node(self, n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self, parent, child):
        self.parent.insert(child, parent)

    def remove_edge(self, n):
        self.parent.pop(n)

    def number_of_nodes(self):
        print("NUMBER OF NODES {}".format(len(self.x)))
        return len(self.x)

    def distance(self, n1, n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        px = (float(x1) - float(x2)) ** 2
        py = (float(y1) - float(y2)) ** 2
        return (px + py) ** (0.5)

    def sample_envir(self):

        x = random.choice(array_x)
        y = random.choice(array_y)
        return x, y

    def nearest(self, n):
        dmin = self.distance(0, n)
        nnear = 0
        for i in range(0, n):
            if self.distance(i, n) < dmin:
                dmin = self.distance(i, n)
                nnear = i
        return nnear

    def collidepoint(self,x2,y2):
        x1=int(x2)
        y1=int(y2)
        if((self.map)[y1][x1][0]==230 ) :
            return True

    def crossObstacle(self, x1, x2, y1, y2):    
           
        for i in range(0, 50):
            u = i / 50
            x = x1 * u + x2 * (1 - u)
            y = y1 * u + y2 * (1 - u)
            if self.map[int(y)][int(x)][0]==230:
                return True
        return False

    def connect(self, n1, n2):
        (x1, y1) = (self.x[n1], self.y[n1])
        (x2, y2) = (self.x[n2], self.y[n2])
        if self.crossObstacle(x1,x2,y1,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1, n2)
            return True
    def search(self,list, platform):
        for i in range(len(list)):
            if list[i] == platform:
                return True
        return False
    def step(self, nnear, nrand, dmax=12):
        d = self.distance(nnear, nrand)
        if d > dmax:
            u = dmax / d
            (xnear, ynear) = (self.x[nnear], self.y[nnear])
            (xrand, yrand) = (self.x[nrand], self.y[nrand])
            (px, py) = (xrand - xnear, yrand - ynear)
            theta = math.atan2(py, px)
            (x, y) = (int(xnear + dmax * math.cos(theta)),
                      int(ynear + dmax * math.sin(theta)))
            if self.search(array_x,x) ==False and self.search(array_y,y)==False:
                x=x-(x%12) 
                y=y-(y%12)
                          
                self.remove_node(nrand)
                if abs(x - self.goal[0]) <= dmax and abs(y - self.goal[1]) <= dmax:
                    self.add_node(nrand, self.goal[0], self.goal[1])
                    self.goalstate = nrand
                    self.goalFlag = True
                else:
                    self.add_node(nrand, x, y)

    def new_parent(self,n,radius=30):
        nodes_of_concern=[]
        for i in range(n):
            if(self.distance(i,n)<radius):
                nodes_of_concern.append(i)
        nnear=self.nearest(n)
        min_dist=self.cost(nnear)    
        parent_node=nnear 
        for ids in nodes_of_concern:
            if(self.cost(ids)<min_dist):
                min_dist=self.cost(ids)
                parent_node=ids
        return parent_node        


    def expand(self):
        n = self.number_of_nodes()
        x, y = self.sample_envir()
        self.add_node(n, x, y)
 
        ids = self.nearest(n)
        self.step(ids, n)
        self.connect(ids, n)
        for i in range(2):
            for j in range(2):
                self.map[self.y[-1]-i][self.x[-1]-j]=[0,0,255]
                self.map[self.y[-1]+i][self.x[-1]+j]=[0,0,255]


    def path_to_goal(self):
        if self.goalFlag:
            self.path = []
            self.path.append(self.goalstate)
            newpos = self.parent[self.goalstate]
            while (newpos != 0):
                self.path.append(newpos)
                newpos = self.parent[newpos]
            self.path.append(0)
        return self.goalFlag

    def getPathCoords(self):
        pathCoords = []
        for node in self.path:
            x, y = (self.x[node], self.y[node])
            pathCoords.append((x, y))
        return pathCoords
def main():

    iteration = 0    
    start = (60,156)
    goal = (420,144)
    img_ = cv2.imread("maze_lv3.png",1)
    img=img_.copy()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if(img[i][j][0]!=230):
                img[i][j][0]=0
                img[i][j][1]=0
                img[i][j][2]=0
    global obstacles
    map = RRTMap(start, goal,img)
    graph = RRTGraph(start, goal,img)
    cv2.namedWindow("window")        
    cv2.imshow('window', img)        
    while (not graph.path_to_goal()):

        graph.expand()
        cv2.imshow("window",img.astype(np.uint8))                 
        iteration += 1  
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break 
    map.drawPath(graph.getPathCoords())
    cv2.imshow("window",img.astype(np.uint8))
    time.sleep(5)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 


if __name__ == '__main__':
    array_form()
    main() 
       
