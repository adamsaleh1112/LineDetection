import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while (True):
    ret, img = vid.read()

    #img = cv2.imread("Parallellines.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.blur(gray, (5, 5))

    ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY)

    edges = cv2.Canny(thresh, 50, 150, apertureSize=3)

    # Masking image at x=300, y=300 for a w and h of 720
    x = 300
    y = 100
    w = h = 720
    mask = np.zeros(edges.shape[:2], np.uint8)
    mask[y:y + h, x:x + w] = 255
    maskimg = cv2.bitwise_and(edges, edges, mask=mask)

    lines = cv2.HoughLinesP(maskimg, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=720)


    if lines is not None:

        # initializing vars required for avg line
        x1avg, x2avg, y1avg, y2avg = 0, 0, 0, 0
        x1sum, x2sum, y1sum, y2sum = 0, 0, 0, 0
        x1counts, y1counts, x2counts, y2counts = 0, 0, 0, 0


        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 4)

            # adding new values to sum vars, adding 1 count to every count var, and calculating avg
            x1sum += x1
            x2sum += x2
            y1sum += y1
            y2sum += y2
            x1counts += 1
            x2counts += 1
            y1counts += 1
            y2counts += 1
            x1avg = x1sum / x1counts
            x2avg = x2sum / x2counts
            y1avg = y1sum / y1counts
            y2avg = y2sum / y2counts

        # drawing avg line at end of for loop
        cv2.line(img, (int(x1avg), int(y1avg)), (int(x2avg), int(y2avg)), (255, 255, 0), 2)

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2)

        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()

# CODE WORKS CITED
# Hough Lines Documentation (Lines 15-22): https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
# Masking (Lines-17-23): https://stackoverflow.com/questions/11492214/opencv-via-python-is-there-a-fast-way-to-zero-pixels-outside-a-set-of-rectangle