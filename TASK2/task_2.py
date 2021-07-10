import cv2 as cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
img = cv2.imread("ball.png")
t = 1
images=[]

cv2.namedWindow("window")
cap = cv2.VideoCapture(0)
k1=1
k2=1
xi=0
yi=0
hi=img.shape[0]-1
x=0
y=0
h=0
w=0
ki=img.shape[1]-1
print(img.shape)
while True:
    _, frm = cap.read()
    img = cv2.imread("ball.png")
    capy=frm.shape[0]
    capx=frm.shape[1]
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img3 = np.zeros_like(frm)
    if(t==1 or(yi<=20)): #if y coordinate of ball (top-left) wrt frame is 0 ---> left wall
        k2=1
        print("BALL HITS THE LEFT WALL")
    if (xi+hi>=capy-20):
        print("GAME OVER TRY AGAIN")
        break
    if(xi+hi>=y-20 and xi+hi<=y+h and yi+ki>=x-20 and yi+ki<=x+w and k1==1 and k2==1):
        k1=-1
        k2=1
        print("BALL HITS YOUR FACE")
       # print("done")
    if(xi+hi>=y-20 and xi+hi<=y+h and yi>=x-20 and yi<=x+w and k1==1 and k2==-1):
        k1=-1
        k2=-1  
        print("BALL HITS YOUR FACE AGAIN")
        #print("done")  
  
    if(yi+hi>=capx-20):
        k2=-1 
        yi-=(yi+hi-capx+1)
        print("BALL HITS RIGHT WALL")
    if(xi==0):
        k1=1
        print("BALL HITS TOP WALL")
    gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)    
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)  
    for (x, y, w, h) in faces:
        cv2.rectangle(frm, (x, y), (x+w, y+h), (255, 0, 0), -1)   
    for i in range(img2.shape[0]):
        for j in range(img2.shape[1]):
            for k in range(3):
                img3[i+xi+20*k1][j+yi+20*k2][k] = img[i][j][k]
                     
    xi+=k1*20
    yi+=k2*20
   # print(x,y,x+w,y+h,xi+hi,yi+ki)
   
    hi=img2.shape[0]-1
    ki=img2.shape[1]-1
   
    t += 1
    Combined = cv2.addWeighted(frm, 0.7,img3, 0.3, 0.1)
    cv2.imshow("window",Combined)
    if cv2.waitKey(30) & 0xFF == ord('q'):
      break
cap.release()    
cv2.destroyAllWindows()
 

