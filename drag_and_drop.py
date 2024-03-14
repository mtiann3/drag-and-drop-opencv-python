import cv2 as cv
from cvzone.HandTrackingModule import HandDetector

cap = cv.VideoCapture(0,cv.CAP_DSHOW )
cap.set(3, 1280)
cap.set(4,720)
detector = HandDetector(detectionCon=0.8)

colorR = (255,0,255)

cx, cy, w, h = 100,100,200,200



while True:


    success, img = cap.read()
    img = cv.flip(img,1)
    hands, img = detector.findHands(img)

    if hands:
        
        hand1 = hands[0]
        lmList1 = hand1['lmList']
        centerPoint1 = hand1['center']

        length, info, img = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)

        print(length)
        if length<30:
            cursor = lmList1[8][:2]


            if cx-w//2<cursor[0]<cx+w//2 and  cy-h//2<cursor[1]<cy+h//2:
                colorR = 0,255,0
                cx,cy = cursor

            else:
                colorR = (255,0,255)

    cv.rectangle(img,(cx-w//2, cy-h//2),(cx+w//2, cy+h//2),colorR,cv.FILLED)

    cv.imshow('Image', img)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

#Release the capture and close all windows
cap.release()
cv.destroyAllWindows()
