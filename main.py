# IMPORT NUMPY AND CV2
import numpy as np # importing numpy, an array library that allows video data to be stored in arrays
import cv2 # importing opencv-python, an image processing library that allows functions such as blur, cropping, etc.

# VIDEO = VIDEO CAPTURE
vid = cv2.VideoCapture(0) 

# WHILE TRUE
while (True):

    # IMAGE PROCESSING
    ret, img = vid.read() # setting img to current frame from video
    kernel = np.ones((1, 1), np.uint8) # setting erosion size for later use (1 by 1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # frame to grayscale
    blur = cv2.blur(gray, (3, 3)) # blur frame 3 pixels
    ret, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV) # thresholding frame (converting to SOLID black and white) but inverted. i.e. dark colors go to white, light colors go to black
    eroded = cv2.erode(thresh, kernel, iterations=1) # eroding frame, which removes one pixel around the white areas, thus thinning the lines which have been turned white with thresholding
    edges = cv2.Canny(eroded, 50, 150, apertureSize=3) # canny edge detectign frame which can detect edges using contrast

    # INTIALIZE VARS FOR MASK
    x = 500 # setting s, y, width and height values for mask
    y = 400
    w = 500
    h = 500
    mask = np.zeros(edges.shape[:2], np.uint8) # extracting values for mask
    mask[y:y + h, x:x + w] = 255 # calculating mask
    maskimg = cv2.bitwise_and(edges, edges, mask=mask) # applying mask

    # DETECT LINES
    lines = cv2.HoughLinesP(maskimg, rho=1, theta=np.pi/180, threshold=70, minLineLength=100, maxLineGap=650) # detecting lines with given parameters

    # IF LINES NOT NONE
    if lines is not None: # if lines are detected
        
        x1avg, x2avg, y1avg, y2avg = 0, 0, 0, 0 # initializing vars required for avg line: avergaes, sums, and counts
        x1sum, x2sum, y1sum, y2sum = 0, 0, 0, 0
        x1counts, y1counts, x2counts, y2counts = 0, 0, 0, 0

        # FOR LINE IN LINES
        for line in lines: # iterates through each line detected 
            x1, y1, x2, y2 = line[0] # defining values from line parameters

            # DRAW LINES
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 4) # draws line by plotting two points (x1,y1) (x2,y2) and draws a line between them

        
        # FOR LINE IN LINES UNDER 2
        for line in lines[:2]: # iterates through each line detected 
            x1, y1, x2, y2 = line[0] # defining values from line parameters

            # CALCULATE MID LINE 
            x1sum += x1 # adding new values to sum vars... 
            x2sum += x2
            y1sum += y1
            y2sum += y2
            x1counts += 1 # adding 1 count to every count var...
            x2counts += 1
            y1counts += 1
            y2counts += 1
            x1avg = x1sum / x1counts # and calculating new averages
            x2avg = x2sum / x2counts
            y1avg = y1sum / y1counts
            y2avg = y2sum / y2counts

        # DRAW MIDLINE
        cv2.line(img, (int(x1avg), int(y1avg)), (int(x2avg), int(y2avg)), (255, 255, 0), 2) # drawing avg line at end of for loop

        # HIGHLIGHT MASK WITH RECTANGLE
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 255, 255), 2) # draws a rectangle using the values specified at the beginning of this script

        cv2.imshow('frame', img) # draws image with overlay
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else: # if no lines detected
        cv2.imshow('frame', img) # draws image without overlay
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()

# CODE WORKS CITED
# Hough Lines Documentation (Lines 15-22): https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html
# Masking (Lines-17-23): https://stackoverflow.com/questions/11492214/opencv-via-python-is-there-a-fast-way-to-zero-pixels-outside-a-set-of-rectangle
