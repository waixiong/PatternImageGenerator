import cv2
import numpy as np


def greater(contour):  # for sorting the contours
    cx, cy = cv2.boundingRect(contour)[:2]
    return cy, cx


def formatColour(colour):  # format the mean colour to whole number
    b = round(colour[0] / 128) * 128
    g = round(colour[1] / 128) * 128
    r = round(colour[2] / 128) * 128
    if b > 255:
        b = 255
    if g > 255:
        g = 255
    if r > 255:
        r = 255
    return b, g, r


# read image
# img = cv2.imread('./testS.jpg')
# img = cv2.imread('./testContours.jpg')
img = cv2.imread('./testImage.jpg')

cloneImg = img.copy()
# imgDraw = np.ones((1000, 1000, 3), np.uint8) * 255

# blur = cv2.GaussianBlur(img, (1, 1), 0)
### cv2.COLOR_BGR2GRAY
## 77 Red 150 Green 28 Blue
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

# hsv = 6 (h) * 5 (sv) = 30 

colorList = []
colorCode = [
    (0, 0, 0), (0, 51, 0), (0, 102, 0), (0, 153, 0), (0, 204, 0), (0, 255, 0),
    (0, 0, 51), (0, 51, 51), (0, 102, 51), (0, 153, 51), (0, 204, 51), (0, 255, 51),
    (0, 0, 102), (0, 51, 102), (0, 102, 102), (0, 153, 102), (0, 204, 102), (0, 255, 102),
    (0, 0, 153), (0, 51, 153), (0, 102, 153), (0, 153, 153), (0, 204, 153), (0, 255, 153),
    (0, 0, 204), (0, 51, 204), (0, 102, 204), (0, 153, 204), (0, 204, 204), (0, 255, 204),
    (0, 0, 255), (0, 51, 255), (0, 102, 255), (0, 153, 255), (0, 204, 255), (0, 255, 255)
]

# blue_lower=np.array([105,170,170],np.uint8) # 200' 
# blue_upper=np.array([135,255,255],np.uint8) # 280' 100% 100%
# blue=cv2.inRange(hsv,blue_lower,blue_upper)
# colorList.append(blue)
# cv2.imshow("thresh", blue)
# cv2.waitKey(0)

# green_lower=np.array([45,170,170],np.uint8) # 200' 
# green_upper=np.array([75,255,255],np.uint8) # 280' 100% 100%
# green=cv2.inRange(hsv,green_lower,green_upper)
# colorList.append(green)
# cv2.imshow("thresh", green)
# cv2.waitKey(0)

# red_lower=np.array([0,170,170],np.uint8) # 200' 
# red_upper=np.array([15,255,255],np.uint8) # 280' 100% 100%
# red1=cv2.inRange(hsv,red_lower,red_upper)
# lower_red = np.array([165,170,170])
# upper_red = np.array([180,255,255])
# red2 = cv2.inRange(hsv, lower_red, upper_red)
# red = red1+red2
# colorList.append(red)
# cv2.imshow("thresh", red)
# cv2.waitKey(0)

# # yellow
# lower=np.array([15,200,200],np.uint8)
# upper=np.array([45,255,255],np.uint8)
# yellow=cv2.inRange(hsv,lower,upper)
# colorList.append(yellow)
# cv2.imshow("thresh", yellow)
# cv2.waitKey(0)
# # cyan
# lower=np.array([75,170,170],np.uint8)
# upper=np.array([105,255,255],np.uint8)
# cyan=cv2.inRange(hsv,lower,upper)
# colorList.append(cyan)
# cv2.imshow("thresh", cyan)
# cv2.waitKey(0)
# # magenta
# lower=np.array([135,170,170],np.uint8)
# upper=np.array([165,255,255],np.uint8)
# magenta=cv2.inRange(hsv,lower,upper)
# colorList.append(magenta)
# cv2.imshow("thresh", magenta)
# cv2.waitKey(0)
from copy import deepcopy
counts = []
for color in colorCode:
    counts.append(0)
    low = list(color)
    high = list(color)
    # low[0] -= 25
    # low[1] -= 25
    # low[2] -= 25
    # high[0] += 26
    # high[1] += 26
    # high[2] += 26
    for l in range(3):
        low[l] -= 25
        if low[l] < 0:
            low[l] = 0
    for h in range(3):
        high[h] += 26
        if high[h] > 255:
            high[h] = 255
    print('\t'+str(low))
    print('\t'+str(high))
    lower=np.array(low,np.uint8)
    upper=np.array(high,np.uint8)
    filterImg=cv2.inRange(img,lower,upper)
    colorList.append(filterImg)
    cv2.imshow("thresh", filterImg)
    print(color)
    print('\t'+str(lower) + str(low))
    print('\t'+str(upper) + str(high))
    cv2.waitKey(0)

ret, thresh = cv2.threshold(imgray, 200, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow("thresh", yellow)
# cv2.waitKey(0)
cv2.imwrite('./filterCopy.jpg', imgray)

triangle = 0
for co in range(len(colorList)):
    color = colorList[co]
    contours, hierarchy = cv2.findContours(color, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        contours.sort(key=greater)
        x, y, w, h = cv2.boundingRect(contours[0])
        row, column, channel = img.shape
        if w == column and h == row:
            contours = contours[1:]

    for i in range(len(contours)):
        print(i)
        shape = "unidentified"
        c = contours[i]
        print('\t'+str(len(c)))
        # print('\t'+str(c))

        # to check is what shape
        # https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
        peri = cv2.arcLength(c, True)
        print('\t'+str(peri))
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        print('\t'+str(approx))
        if len(approx) == 3:
            shape = "triangle"
            print('is triangle')
            triangle += 1
            counts[co] += 1
            # draw image for every contour detected
            # cloneImg = img.copy()
            # newImage = cv2.drawContours(cloneImg, contours, i, (0, 255, 0), 3)
            # title = f'{shape} {i}'
            # cv2.imshow(title, newImage)
            # cv2.waitKey(0)

            # draw contour with mask to find the mean value of colour of the contour
            # https://stackoverflow.com/questions/54316588/get-the-average-color-inside-a-contour-with-open-cv/54317652
            mask = np.zeros(imgray.shape[:2], np.uint8)
            maskImage = cv2.drawContours(mask, contours, i, 255, -1)

            # erode the mask slightly to ensure statistics are only being computed for the masked region and that no
            # background is accidentally included
            mask = cv2.erode(mask, None, iterations=5)
            mean_val = cv2.mean(cloneImg, mask=mask)
            # print(mean_val)

            # format rgb to whole number
            b, g, r = formatColour(mean_val)
            print('\t'+str(r)+', '+str(g)+', '+str(b))
            imgDraw = np.ones((1000, 1000, 3), np.uint8) * 255
            cv2.drawContours(imgDraw, [approx], 0, (b, g, r), -1)
            cv2.imshow("thresh", imgDraw)
            cv2.waitKey(0)

print(triangle)
for i in range(len(colorCode)):
    print(colorCode[i])
    print(counts[i])

# # remove the totalChar in front of binary and random characters that is appended to the end of array
# # totalChar = int(dataTransferred[:16], 2)
# # secretBin = dataTransferred[16:16+(totalChar*7)]
# # secretMessage = ""

# # for i in range(0, len(secretBin), 7):
# #     secretMessage = secretMessage + chr(int(secretBin[i:i + 7], 2))

# # print(secretMessage)

# # newImage = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
# # cv2.imshow("contours", newImage)
# # cv2.waitKey(0)

# cv2.imshow("decode", imgDraw)
# cv2.waitKey(0)