import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
#kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (3,3))
#fgbg = cv.bgsegm.createBackgroundSubtractorMOG()
fgbg=cv.createBackgroundSubtractorMOG2()
#fgbg = cv.bgsegm.BackgroundSubtractorGMG()
#fgbg = cv.createBackgroundSubtractorMOG2(detectShadows=True)
#fgbg = cv.createBackgroundSubtractorKNN(detectShadows=True)
while True:
    ret, frame = cap.read()
    if frame is None:
        break
    fgmask = fgbg.apply(frame)
    img2=cv.cvtColor(fgmask,cv.COLOR_GRAY2BGR)
    IMG3=cv.cvtColor(img2,cv.COLOR_BGR2HSV)
    dimensions = fgmask.shape[:2]
    print(fgmask.shape)
    lower = np.array([0, 0, 0])
    upper = np.array([0, 0, 255])
    #img2 = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    mask = cv.inRange(IMG3, lower, upper)
    output = cv.bitwise_and(frame, frame, mask=mask)
    output_ = cv.cvtColor(output, cv.COLOR_BGR2GRAY)
    img = output_.copy()
    img=cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    ret,thresh = cv.threshold(img,127,255,0)
    contours,hierarchy = cv.findContours(thresh,  cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv.minAreaRect(cnt)
        box = cv.boxPoints(rect)
        box = np.int0(box)
        #print(box)
  #  obstacles.append(box)
        cv.drawContours(frame, [box], 0, (0, 0, 255), 2)
    #fgmask = cv.morphologyEx(fgmask, cv.MORPH_OPEN, kernel)

    cv.imshow('Frame', frame)
    cv.imshow('FG MASK Frame', fgmask)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break
cap.release()
cv.destroyAllWindows()