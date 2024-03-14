# This file is used for learning how to use the multiple hand gesture control with OpenCV in Python with the CVZone library.

import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

# Define video capture method
cap = cv.VideoCapture(0,cv.CAP_DSHOW )
# Hand detector method
detector = HandDetector(detectionCon=0.8)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, flipType=False)
    # hands, img = detector.findHands(img, draw=False)
    
    if hands:
        # Hand1
        hand1 = hands[0]
        # List of 21 landmark points
        lmList1 = hand1['lmList']
        # Bounding box info (x,y,w,h)
        bbox1 = hand1['bbox']
        # Center of the hand (cx,cy)
        centerPoint1 = hand1['center']
        # Hand type (left or right)
        handType1 = hand1['type']

        # print(len(lmList1), lmList1)
        # print(bbox1)
        # print(centerPoint1)
        # print(handType1)
        fingers1 = detector.fingersUp(hand1)
        # distance between middle and pointer finger of first hand.
        # length, info, img = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)

        if len(hands)==2:
            # types of data you can find: 
            # declare hand
            hand2 = hands[1]

            # set of coordinates of points on hand
            lmList2 = hand2['lmList']

            # bbox of hand x, y, z
            bbox2 = hand2['bbox']

            # center point of hand
            centerPoint2 = hand2['center']

            # hand type, left or right
            handType2 = hand2['type']

            # detect which fingers are up (not closed)
            fingers2 = detector.fingersUp(hand2)
            
            # Distance between pointer fingers of both hands.
            # length, info, img = detector.findDistance(lmList1[8][:2], lmList2[8][:2], img)

            # distance between center of both hands
            length, info, img = detector.findDistance(centerPoint1, centerPoint2, img)



    cv.imshow('Image', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


#Release the capture and close all windows
cap.release()
cv.destroyAllWindows()
