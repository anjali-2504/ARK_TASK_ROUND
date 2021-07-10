import cv2 as cv2
import numpy as np


img = cv2.imread("/home/anjali/winterworkshop/treasure_mp3.png")
string = ""

print(img.shape)
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
fp = open('/home/anjali/audio_byte.txt', 'wb')
for i in range(img.shape[0]):
    for j in range(img.shape[1]):
        fp.write(img2[i][j])
         

fp.close()    


cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.imshow('image',img.astype(np.uint8))
cv2.waitKey(0)
cv2.destroyAllWindows() 