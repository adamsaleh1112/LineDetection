import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while (True):
    ret, img = vid.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 250, minLineLength=50, maxLineGap=10)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 5)
            cv2.flip(img, 1)

        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()

# CODE WORKS CITED
# Hough Lines Documentation (Lines 15-22): https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html