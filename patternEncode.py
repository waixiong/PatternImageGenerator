import numpy as np
from Delaunator import Delaunator
import time
import cv2

import patternECC

def imgGenerator(delaunator, points, numberData, maxSize):
    excessData = 0
    dd2 = 0
    img = np.ones((maxSize, maxSize, 3), np.uint8) * 255
    triangles = delaunator.triangles

    for i in range(len(triangles)//3):
        pointA = triangles[i*3]
        pointB = triangles[i*3+1]
        pointC = triangles[i*3+2]

        triangle_cnt = np.array( [(points[pointA][0], points[pointA][1]), (points[pointB][0], points[pointB][1]), (points[pointC][0], points[pointC][1])] )

        # method 2: 32 (8) [all]
        if numberData != 0:
            rgb = (numberData % 512)
            numberData = numberData // 512
            r = rgb % 8
            g = (rgb // 8) % 8
            b = (rgb // 64) % 8
            cv2.drawContours(img, [triangle_cnt], 0, (b*32+16, g*32+16, r*32+16), -1)

            # dataRGB = b
            # dataRGB = dataRGB*8 + g
            # dataRGB = dataRGB*8 + r
            # numberData = numberData + dataRGB * multipleCounter
            # multipleCounter *= 512
        else:
            r = np.random.randint(0,8)
            g = np.random.randint(0,8)
            b = np.random.randint(0,8)
            if excessData == 0:
                excessData = 1
            excessData *= 512
            cv2.drawContours(img, [triangle_cnt], 0, (b*32+16, g*32+16, r*32+16), -1)
    return img

def generatePoints(numberData, maxSize):
    #create random points
    points = []
    for x in range(maxSize//50 + 1):
        for y in range(maxSize//50 + 1):
            xp = x * 50
            yp = y * 50
            if xp >= maxSize :
                xp = maxSize-1
            if yp >= maxSize :
                yp = maxSize-1
            points.append( [xp, yp] )
    size_on_line = 1
    dd2 = 0
    
    # point adjustment on data
    for point in points:
        if point[0] > 0 and point[0] < maxSize - 1:
            xr = (numberData % 8 - 3) * 5
            dd2 = dd2 + (numberData % 8) * size_on_line
            numberData = numberData // 8
            # print('\t'+str(dd2))
            point[0] += xr
            size_on_line *= 8
        if point[1] > 0 and point[1] < maxSize - 1:
            yr = (numberData % 8 - 3) * 5
            dd2 = dd2 + (numberData % 8) * size_on_line
            numberData = numberData // 8
            # print('\t'+str(dd2))
            point[1] += yr
            size_on_line *= 8
    print(dd2)
    print(size_on_line)
    # print('line: '+str((size_on_line.bit_length() + 7) // 8) + ' bytes')
    return points, numberData

def calculateImgSize(byteData):
    maxSize = 0
    
    pointsByte = 0
    colorsByte = 0
    while len(byteData) > (pointsByte+colorsByte):
        maxSize += 250
        # points
        numOfPoints = pow(maxSize//50 + 1, 2)
        # print(numOfPoints)
        pointsByte = 0.64 * numOfPoints

        # color
        # numOfTriangle = numOfPoints * 1.28
        numOfTriangle = round(2 * ((maxSize//50) ** 2) * 0.96)
        # print('tri: '+str(numOfTriangle))
        # method 2: 15 (18)
        # TODO: method
        colorsByte = (int(pow(512, int(numOfTriangle))).bit_length() + 7) // 8
    # print('\tLine bytes: '+str(pointsByte))
    # print('\tColor bytes: '+str(colorsByte))
    # print('\tEstimate bytes: '+str(pointsByte+colorsByte))
    return maxSize

def encode(byteData, outputfile):
    byteData = patternECC.encodeWithReedSolo(byteData)
    byteData.append(0x1A)
    byteData.append(0x1A)
    byteData.append(0x1A)
    print('use default color set encode')
    maxSize = calculateImgSize(byteData)
    numberData = int.from_bytes(byteData, byteorder='little')
    
    points, numberData = generatePoints(numberData, maxSize)
    # print(points)
    delaunator = Delaunator(points)

    img = imgGenerator(delaunator, points, numberData, maxSize)
    cv2.imshow("triangle", img)
    cv2.waitKey(0)
    cv2.imwrite(outputfile, img)
