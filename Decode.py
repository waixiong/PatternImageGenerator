import cv2
import numpy as np


def greater(contour):  # for sorting the contours
    cx, cy = cv2.boundingRect(contour)[:2]
    return cy, cx


def formatColour(colour):  # format the mean colour to whole number
    b = round(colour[0] // 32) * 32 + 16
    g = round(colour[1] // 32) * 32 + 16
    r = round(colour[2] // 32) * 32 + 16
    if b > 255:
        b = 255
    if g > 255:
        g = 255
    if r > 255:
        r = 255
    return b, g, r


# read image
img = cv2.imread('./Output.jpg')
# img = cv2.imread('./testS.jpg')
cloneImg = img.copy()
imgDraw = np.ones(img.shape, np.uint8) * 255

# cv2.imwrite("canny.jpg", cv2.Canny(img, 200, 300))
# cv2.imshow("canny", cv2.imread("canny.jpg"))
# cv2.waitKey(0)

# blur = cv2.GaussianBlur(img, (1, 1), 0)
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("imgray", imgray)
# cv2.waitKey(0)
ret, thresh = cv2.threshold(imgray, 200, 200, 0)
# cv2.imshow("thresh", thresh)
# cv2.waitKey(0)
# contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

low_threshold = np.array(( 48-16, 48-16, 176-16 ), dtype=np.uint8, ndmin=1)
threshold = np.array(( 48, 48, 176), dtype=np.uint8, ndmin=1)
high_threshold = np.array(( 48+15, 48+15, 176+15 ), dtype=np.uint8, ndmin=1)
a = cv2.inRange(img, low_threshold, high_threshold)
aa = cv2.cvtColor(a, cv2.COLOR_GRAY2BGR)
i = img & aa
cv2.imshow("img", img)
cv2.imshow("a", a)
cv2.waitKey(0)

contours, hierarchy = cv2.findContours(a, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# exit(0)

contours.sort(key=greater)
# x, y, w, h = cv2.boundingRect(contours[0])
# row, column, channel = img.shape
# if w == column and h == row:
#     contours = contours[1:]

dataTransferred = ""
points = []

print('contours: '+str(len(contours)))
for i in range(len(contours)):
    # print(i)
    shape = "unidentified"
    c = contours[i]
    # print('\t'+str(len(c)))
    # print('\t'+str(c))

    # to check is what shape
    # https://www.pyimagesearch.com/2016/02/08/opencv-shape-detection/
    peri = cv2.arcLength(c, True)
    # print('\t'+str(peri))
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)
    # print('\t'+str(approx[0][0][0]))
    if len(approx) == 3:
        shape = "triangle"
        print('is triangle')
        for p in range(len(approx)):
            points.append([ approx[p][0][0], approx[p][0][1] ])
    elif len(approx) > 3 and peri >= 24:
        shape = "shape"
        print('is shape')
        for p in range(len(approx)):
            points.append([ approx[p][0][0], approx[p][0][1] ])

    # draw image for every contour detected
    # cloneImg = img.copy()
    # newImage = cv2.drawContours(cloneImg, contours, i, (0, 255, 0), 3)
    # title = f'{shape} {i}'
    # cv2.imshow(title, newImage)
    # cv2.waitKey(0)

    # draw contour with mask to find the mean value of colour of the contour
    # https://stackoverflow.com/questions/54316588/get-the-average-color-inside-a-contour-with-open-cv/54317652
    mask = np.zeros(imgray.shape[:2], np.uint8)
    cv2.imshow("mask1", mask)
    # cv2.waitKey(0)
    mask = cv2.drawContours(mask, contours, i, 255, -1)
    cv2.imshow("mask2", mask)
    cv2.waitKey(0)

    # erode the mask slightly to ensure statistics are only being computed for the masked region and that no
    # background is accidentally included
    # mask = cv2.erode(mask, None, iterations=3)
    # cv2.imshow("mask3", mask)
    # cv2.waitKey(0)
    mean_val = cv2.mean(cloneImg, mask=mask)
    # print(mean_val)

    # format rgb to whole number
    b, g, r = formatColour(mean_val)
    print('\t'+str(r)+', '+str(g)+', '+str(b))
    cv2.drawContours(imgDraw, [approx], 0, (b, g, r), -1)

# print("points: "+str(points))


# remove the totalChar in front of binary and random characters that is appended to the end of array
# totalChar = int(dataTransferred[:16], 2)
# secretBin = dataTransferred[16:16+(totalChar*7)]
# secretMessage = ""

# for i in range(0, len(secretBin), 7):
#     secretMessage = secretMessage + chr(int(secretBin[i:i + 7], 2))

# print(secretMessage)

# newImage = cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
# cv2.imshow("contours", newImage)
# cv2.waitKey(0)

cv2.imshow("decode", imgDraw)
cv2.waitKey(0)
cv2.imwrite('./decodeCopy.jpg', imgDraw)