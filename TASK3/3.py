import cv2 as cv2
import numpy as np
 

img = cv2.imread("Level1.png")
string = ""
string1= ""
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
for i in range(8):
    for j in range(177):
        string+=chr(img2[i][j])
        if(img2[i][j]==58):
            print(i,j)
            #string+="   Anjali "      

 

img3= img2.copy()
img4=[]

 

for i in range(6,7):
    for j in range(94,177):
        string1+=chr(img2[i][j])
        img4.append(img3[i][j])
for i in range(7,177):
    for j in range(177):
        string1+=chr(img2[i][j])
        img4.append(img3[i][j])        

 

print(len(img4))
print(chr(img4[0]))
new=np.array(img4)
print(string)
#new1=new[:30000].reshape(150,200)
new1=new[:30000].reshape(200,150)
new2 = cv2.cvtColor(new1, cv2.COLOR_GRAY2BGR)
print(new2.shape)
cv2.imwrite("lv2.jpg", new2)
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('image',new1.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows() 

