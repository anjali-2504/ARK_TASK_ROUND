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
class square(object):

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return square(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

num_explored=0   
dir4 = [square(0, -12), square(0, 12),square(-12, 0),square(12, 0)]
h, w = img.shape[:2]
def BFS(s, e):

    global img, img1,h, w,num_explored
    const = 10000
   # print(s,e)

    found = False
    q = []
    v = [[0 for j in range(w)] for i in range(h)]
    parent = [[square() for j in range(w)] for i in range(h)]

    q.append(s)
    print(len(q))
    num_explored+=1

    v[s.y][s.x] = 1
    while len(q) > 0:
        cv2.imshow("IMAGE", img)
        cv2.waitKey(1)
        p = q.pop(0)
        for d in dir4:
            kx=0
            ky=0
            cell = p + d
            if(d.x>0):
                kx=6
                ky=0
            elif (d.x<0):
                kx=-6
                ky=0
            else:
                if(d.x==0):
                    kx=0
                    if(d.y>0):
                        ky=6
                    elif(d.y<0):
                        ky=-6        
            obs=square(kx,ky)
            cell1= p + obs
            #print(cell.x,w,cell.y,h)
            if (cell.x >= 12 and cell.x <= 444 and cell.y >= 12 and cell.y <=156 and v[cell.y][cell.x] == 0 and 
                    (img1[cell1.y][cell1.x][0] == 0 and img1[cell1.y][cell1.x][1] == 0 and img1[cell1.y][cell1.x][2] == 0)):
                q.append(cell)
                num_explored+=1
                v[cell.y][cell.x] = v[p.y][p.x] + 1  # Later
            
                #img[cell.y][cell.x]=[0,255,0]
                for i in range(2):
                    for j in range(2):
                        img[cell.y-i][cell.x-j]=[0,0,255]
                        img[cell.y+i][cell.x+j]=[0,0,255]

                parent[cell.y][cell.x] = p
                if cell == e:
                    found = True
                    del q[:]
                    break

    path = []
    if found:
        p = e
        while p != s:
            path.append(p)
            p = parent[p.y][p.x]
        path.append(p)
        path.reverse()

        for p in path:
            for i in range(2):
                    for j in range(2):
                        img[p.y-i][p.x-j]=[0,255,0]
                        img[p.y+i][p.x+j]=[0,255,0]

        print("Path Found")
    else:
        print("Path Not Found")            
      
#cv2.imshow('image',img.astype(np.uint8))
start=square(60,156)
end=square(420,144)
img1=img.copy()
BFS(start,end)
print(img.shape)
print(num_explored)

cv2.imshow("IMAGE", img)
cv2.waitKey(0)
cv2.destroyAllWindows() 
