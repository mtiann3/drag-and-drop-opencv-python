import cv2
from cvzone.HandTrackingModule import HandDetector


# index 1 for mac webcam.
# Define video capture
cap = cv2.VideoCapture(1)

# Setting width and height
cap.set(3,1280)
cap.set(4,720)

# Defining hand detector.
detector = HandDetector(detectionCon=0.8)

while True:
    # Display each frame
    success, img = cap.read()
    cv2.imshow('Image', img)
    cv2.waitKey(1)