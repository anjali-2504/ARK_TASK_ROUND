import cv2
import matplotlib.pyplot as plt
import numpy as np
img_ = cv2.imread('maze_lv3.png') # read an image from a file using
img=img_.copy()

for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        #for k in range(3):
        if(img[i][j][0]!=230):
            img[i][j][0]=0
            img[i][j][1]=0
            img[i][j][2]=0
cv2.namedWindow("IMAGE")

#Helper functions and classes
class Vertex:
    def __init__(self,x_coord,y_coord):
        self.x=x_coord
        self.y=y_coord
        self.d=float('inf') #distance from source
        self.parent_x=None
        self.parent_y=None
        self.processed=False
        self.index_in_queue=None

def neighbors( mat,state):
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
            if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img[c][r+6][0] == 0 and img[c][r+6][1] == 0 and img[c][r+6][2] == 0)  and not mat[c][r].processed:
                result.append( mat[c][r])

        if r==row+12:
            if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img[c][r-6][0] == 0 and img[c][r-6][1] == 0 and img[c][r-6][2] == 0) and not mat[c][r].processed:
                result.append( mat[c][r])   

        if c==col-12:
            if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img[c+6][r][0] == 0 and img[c+6][r][1] == 0 and img[c+6][r][2] == 0) and not mat[c][r].processed:
                result.append(  mat[c][r])

        if c==col+12:
            if r >= 12 and r <= 444 and c >= 12 and c <=156 and  (img[c-6][r][0] == 0 and img[c-6][r][1] == 0 and img[c-6][r][2] == 0) and not mat[c][r].processed:
                result.append( mat[c][r])        

    return result


def bubble_up(queue, index):
    if index <= 0:
        return queue
    p_index=(index-1)//2
    if queue[index].d < queue[p_index].d:
            queue[index], queue[p_index]=queue[p_index], queue[index]
            queue[index].index_in_queue=index
            queue[p_index].index_in_queue=p_index
            queue = bubble_up(queue, p_index)
    return queue
    
def bubble_down(queue, index):
    length=len(queue)
    lc_index=2*index+1
    rc_index=lc_index+1
    if lc_index >= length:
        return queue
    if lc_index < length and rc_index >= length: #just left child
        if queue[index].d > queue[lc_index].d:
            queue[index], queue[lc_index]=queue[lc_index], queue[index]
            queue[index].index_in_queue=index
            queue[lc_index].index_in_queue=lc_index
            queue = bubble_down(queue, lc_index)
    else:
        small = lc_index
        if queue[lc_index].d > queue[rc_index].d:
            small = rc_index
        if queue[small].d < queue[index].d:
            queue[index],queue[small]=queue[small],queue[index]
            queue[index].index_in_queue=index
            queue[small].index_in_queue=small
            queue = bubble_down(queue, small)
    return queue

def get_distance(img,u,v):
    return 0.1 + (float(img[v][0])-float(img[u][0]))**2+(float(img[v][1])-float(img[u][1]))**2+(float(img[v][2])-float(img[u][2]))**2


def find_shortest_path(img,src,dst):
    pq=[] #min-heap priority queue
    source_x=src[0]
    source_y=src[1]
    dest_x=dst[0]
    dest_y=dst[1]
    imagerows,imagecols=img.shape[0],img.shape[1]
    matrix = np.full((imagerows, imagecols), None) #access by matrix[row][col]
    for r in range(12,157,12):
        for c in range(12,445,12):
            matrix[r][c]=Vertex(c,r)
            matrix[r][c].index_in_queue=len(pq)
            pq.append(matrix[r][c])
    matrix[source_y][source_x].d=0
    pq=bubble_up(pq, matrix[source_y][source_x].index_in_queue)
    while len(pq) > 0:
        cv2.imshow("IMAGE",img)
        cv2.waitKey(1)
        u=pq[0]
        u.processed=True
        pq[0]=pq[-1]
        pq[0].index_in_queue=0
        pq.pop()
        pq=bubble_down(pq,0)
        neig = neighbors(matrix,(u.x,u.y))
        for v in neig:
            dist=get_distance(img,(u.y,u.x),(v.y,v.x))
            if u.d + dist < v.d:
                v.d = u.d+dist
                v.parent_x=u.x
                v.parent_y=u.y
                idx=v.index_in_queue
                pq=bubble_down(pq,idx)
                pq=bubble_up(pq,idx)
                          
    path=[]
    iter_v=matrix[dest_y][dest_x]
    path.append((dest_x,dest_y))
    while(iter_v.y!=source_y or iter_v.x!=source_x):
        path.append((iter_v.x,iter_v.y))
        iter_v=matrix[iter_v.parent_y][iter_v.parent_x]

    path.append((source_x,source_y))

    x0,y0=path[0]
    for vertex in path[1:]:
        x1,y1=vertex
        cv2.line(img,(x0,y0),(x1,y1),(255,0,0),2)
        x0,y0=vertex
        cv2.imshow("IMAGE",img)
        cv2.waitKey(1)    
p = find_shortest_path(img, (60,156), (420,144))
cv2.waitKey(0)
cv2.destroyAllWindows()
