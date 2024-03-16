import cv2 as cv
from cvzone.HandTrackingModule import HandDetector
import cvzone
import numpy as np

# Initialize the webcam
cap = cv.VideoCapture(0, cv.CAP_DSHOW)
cap.set(3, 1280)  # Set width
cap.set(4, 720)   # Set height

# Initialize hand detector from cvzone library
detector = HandDetector(detectionCon=0.8)

# Define a color for the rectangle
colorR = (255, 0, 255)

# Initialize initial position and size of the rectangle
cx, cy, w, h = 100, 100, 200, 200


# Class for a draggable rectangle
class DragRect():
    def __init__(self, posCenter, size=[200, 200]):
        self.posCenter = posCenter
        self.size = size

    def update(self, cursor):
        cx, cy = self.posCenter
        w, h = self.size

        # If the finger is in the rectangle region, update position
        if cx - w // 2 < cursor[0] < cx + w // 2 and cy - h // 2 < cursor[1] < cy + h // 2:
            self.posCenter = cursor


# Create a list of draggable rectangles for replication
rectList = []
for x in range(5):
    rectList.append(DragRect([x * 250 + 150, 150]))

# Main loop
while True:
    # Read frame from webcam
    success, img = cap.read()
    img = cv.flip(img, 1)  # Flip horizontally for mirror effect

    # Find hands in the frame
    hands, img = detector.findHands(img)

    if hands:
        # Get the details of the first hand
        hand1 = hands[0]
        lmList1 = hand1['lmList']
        centerPoint1 = hand1['center']

        # Calculate distance between thumb and index finger
        length, info, img = detector.findDistance(lmList1[8][:2], lmList1[12][:2], img)

        # If distance between fingers is less than a threshold, treat it as cursor and update rectangles
        if length < 30:
            cursor = lmList1[8][:2]
            for rect in rectList:
                rect.update(cursor)

    # Create a transparent overlay for drawing rectangles
    imgNew = np.zeros_like(img, np.uint8)

    # Draw rectangles on the overlay
    for rect in rectList:
        cx, cy = rect.posCenter
        w, h = rect.size
        cv.rectangle(imgNew, (cx - w // 2, cy - h // 2), (cx + w // 2, cy + h // 2), colorR, cv.FILLED)
        cvzone.cornerRect(imgNew, (cx - w // 2, cy - h // 2, w, h), 20, rt=0)

    # Combine original frame and overlay with transparency
    out = img.copy()
    alpha = 0.5
    mask = imgNew.astype(bool)
    out[mask] = cv.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]

    # Display the output frame
    cv.imshow('Image', out)

    # Break the loop if 'q' is pressed
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv.destroyAllWindows()
