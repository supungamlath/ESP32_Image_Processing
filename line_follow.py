import math
import cv2
import numpy as np


def detect_centering(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, 140, 255, cv2.THRESH_BINARY)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(
        thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)
        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        else:
            cx, cy = 1280, 720

        cv2.line(frame, (cx, 0), (cx, 720), (255, 0, 0), 1)
        cv2.line(frame, (0, cy), (1280, cy), (255, 0, 0), 1)
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 1)
        return cx, cy
    return None


def detect_color_squares(frame):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0, 20, 50])
    upper_red = np.array([30, 255, 255])
    lower_green = np.array([50, 20, 50])
    upper_green = np.array([80, 255, 255])
    lower_blue = np.array([100, 50, 50])
    upper_blue = np.array([140, 255, 255])

    # Threshold the HSV image to get binary images for each color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours for each color
    contours_red, _ = cv2.findContours(
        mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_green, _ = cv2.findContours(
        mask_green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(
        mask_blue, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours and label each color
    for cnt in contours_red:
        area = cv2.contourArea(cnt)
        if (area > 8000):
            cv2.drawContours(frame, [cnt], 0, (0, 0, 255), 2)
            # cv2.putText(frame, str(cv2.contourArea(cnt)), (cnt[0][0][0], cnt[0][0][1]),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            print("Red")
            return "red"

    for cnt in contours_green:
        area = cv2.contourArea(cnt)
        if (area > 8000):
            cv2.drawContours(frame, [cnt], 0, (0, 255, 0), 2)
            # cv2.putText(frame, str(cv2.contourArea(cnt)), (cnt[0][0][0], cnt[0][0][1]),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            print("Green")
            return "green"

    for cnt in contours_blue:
        area = cv2.contourArea(cnt)
        if (area > 8000):
            cv2.drawContours(frame, [cnt], 0, (255, 0, 0), 2)
            # cv2.putText(frame, str(cv2.contourArea(cnt)), (cnt[0][0][0], cnt[0][0][1]),
            #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print("Blue")
            return "blue"

    return None


def detect_lines(frame):
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Color thresholding
    ret, thresh = cv2.threshold(blur, 140, 255, cv2.THRESH_BINARY)

    # Find the contours of the frame
    contours, hierarchy = cv2.findContours(
        thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)

        # Approximate contour with a polygonal curve
        epsilon = 0.01 * cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, epsilon, True)
        print(len(approx))
        # Draw approximated polygon
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 1)

    return None


def detect_lines_hough(frame):
    # Load the image
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Threshold the image to create a binary image
    _, binary_img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)

    # Apply morphological operations to enhance the lines
    kernel = np.ones((5, 5), np.uint8)
    binary_img = cv2.morphologyEx(binary_img, cv2.MORPH_CLOSE, kernel)

    # Detect lines using HoughLines
    # lines = cv2.HoughLines(binary_img, 4, np.pi / 180, 900, None, 0, 0)

    # Draw the lines on the original image
    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         rho = lines[i][0][0]
    #         theta = lines[i][0][1]
    #         a = math.cos(theta)
    #         b = math.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
    #         pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
    #         # cv2.line(frame, pt1, pt2, (0, 255, 0), 1, cv2.LINE_AA)

    # Display the output image
    cv2.imshow("Output", binary_img)
