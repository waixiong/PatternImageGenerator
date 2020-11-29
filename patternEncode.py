import numpy as np
from Delaunator import Delaunator
import time
import cv2
import os
import math

import patternECC

size = 0

def imgGenerator(delaunator, points, numberData, maxSize):
    global size
    excessData = 0
    colorData = 0
    dd2 = 0
    img = np.ones((maxSize, maxSize, 3), np.uint8) * 255
    triangles = delaunator.triangles

    # print('\ta  size: '+str(size.bit_length() / 8))
    # print('\ta color: '+str(colorData.bit_length() / 8))

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
        size = (size + 1) * 512 - 1
        colorData = (colorData + 1) * 512 - 1
        # print('\ta  size: '+str(size.bit_length() / 8))
        # print('\ta color: '+str(colorData.bit_length() / 8))

    print('Color byte : '+str(colorData.bit_length() / 8))
    print('Total byte : '+str(size.bit_length() / 8))
    return img

def generatePoints(numberData, maxSize):
    global size
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
    size_on_line = 0
    dd2 = 0
    
    # point adjustment on data
    for point in points:
        if point[0] > 0 and point[0] < maxSize - 1:
            xr = (numberData % 8 - 3) * 5
            dd2 = dd2 + (numberData % 8) * size_on_line
            numberData = numberData // 8
            # print('\t'+str(dd2))
            point[0] += xr
            size_on_line = (size_on_line + 1) * 8 - 1
        if point[1] > 0 and point[1] < maxSize - 1:
            yr = (numberData % 8 - 3) * 5
            dd2 = dd2 + (numberData % 8) * size_on_line
            numberData = numberData // 8
            # print('\t'+str(dd2))
            point[1] += yr
            size_on_line = (size_on_line + 1) * 8 - 1
    # print(dd2)
    print('\tgenerate points')
    print('Points byte : '+str((size_on_line.bit_length()) / 8))
    size += size_on_line
    # print('line: '+str((size_on_line.bit_length() + 7) // 8) + ' bytes')
    return points, numberData

def calculateImgSize(byteData):
    global size
    maxSize = 0
    
    pointsByte = 0
    colorsByte = 0
    while patternECC.estimateLengthWithReedSolo(byteData) > (pointsByte+colorsByte):
        maxSize += 250
        # points
        numOfPoints = pow(maxSize//50 + 1, 2)
        # print(numOfPoints)
        pointsNumber = pow( 8 * 8 , pow(maxSize//50 - 1, 2) ) * pow( 8 , (maxSize//50 - 1) * 4 ) - 1
        pointsByte = int(pointsNumber).bit_length() / 8

        # color
        # numOfTriangle = numOfPoints * 1.28
        numOfTriangle = round(2 * ((maxSize//50) ** 2))
        # print('tri: '+str(numOfTriangle))
        # method 2: 15 (18)
        # TODO: method
        # colorsByte = (int(pow(512, int(numOfTriangle))).bit_length() + 7) // 8
        colorsByte = (int(pow(512, int(numOfTriangle)) - 1).bit_length()) / 8
        print('\tEstimate Points: '+str(pointsByte))
        print('\tEstimate Colors: '+str(colorsByte))
        print('\tEstimate CurrentByte: '+str(pointsByte+colorsByte))
    # print('\tLine bytes: '+str(pointsByte))
    # print('\tColor bytes: '+str(colorsByte))
    # print('\tEstimate bytes: '+str(pointsByte+colorsByte))
    return maxSize, pointsByte+colorsByte

def encode(byteData, outputfile):
    global size
    size = 0
    byteData += b'\x1A'
    maxSize, length = calculateImgSize(byteData)
    print(len(byteData))
    byteData = patternECC.encodeWithReedSolo(byteData, length = length)
    if len(byteData) == 0:
        print('CURRENTLY PROGRAM ONLY ALLOW 51 CHARACTERS')
        exit(0)
    # print(0)
    # byteData = patternECC.encodeWithReedSolo(byteData)
    print('use default color set encode')
    numberData = int.from_bytes(byteData, byteorder='little')
    
    points, numberData = generatePoints(numberData, maxSize)
    delaunator = Delaunator(points)

    img = imgGenerator(delaunator, points, numberData, maxSize)
    cv2.imshow("triangle", img)
    cv2.waitKey(0)
    cv2.imwrite(outputfile, img)
