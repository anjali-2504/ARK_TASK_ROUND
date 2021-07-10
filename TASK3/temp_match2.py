import numpy as np
from cv2 import cv2
from matplotlib import pyplot as plt

clr_img = cv2.imread('zucky_elon.png')
gry_img=cv2.cvtColor(clr_img, cv2.COLOR_BGR2GRAY) 
template = cv2.imread('lv2.jpg',0)
h , w= template.shape
print(template.shape)
img2 =clr_img.copy()
result = cv2.matchTemplate(gry_img, template,cv2.TM_CCOEFF_NORMED)
#print(result)
# Declare a threshold   
threshold = 0.999
# Store the coordinates of matched region in a numpy array   
loc = np.where( result>= threshold)   
# Draw a rectangle around the matched region. 
# #min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(img2,top_left, bottom_right, 255, 2)
# Now display the final matched template image   
cv2.imshow('Detected',img2.astype(np.uint8)) 
cv2.waitKey(0)
cv2.destroyAllWindows() 

