import numpy as np
from Delaunator import Delaunator
import time
import cv2

start_time = time.process_time()
maxSize = 500

# print(cv2.__version__)

# 1KB input
byteData = b''
with open("1KB", "rb") as f:
    byte = f.read(1)
    while byte:
        # print(byte)
        byteData += byte
        byte = f.read(1)
numberData = int.from_bytes(byteData, byteorder='little')
print('read data')
print('input: '+str((numberData.bit_length() + 7) // 8) + ' bytes')
excessData = 0

#create random points
points = []
for x in range(maxSize//25 + 1):
    for y in range(maxSize//25 + 1):
        xp = x * 25
        yp = y * 25
        if xp >= maxSize :
            xp = maxSize-1
        if yp >= maxSize :
            yp = maxSize-1
        points.append( [xp, yp] )
# points = [
#     [000, 000], [000, 100], [000, 200], [000, 300], [000, 400], [000, 500], [000, 600], [000, 700], [000, 800], [000, 900], [000, 999],
#     [100, 000], [100, 100], [100, 200], [100, 300], [100, 400], [100, 500], [100, 600], [100, 700], [100, 800], [100, 900], [100, 999],
#     [200, 000], [200, 100], [200, 200], [200, 300], [200, 400], [200, 500], [200, 600], [200, 700], [200, 800], [200, 900], [200, 999],
#     [300, 000], [300, 100], [300, 200], [300, 300], [300, 400], [300, 500], [300, 600], [300, 700], [300, 800], [300, 900], [300, 999],
#     [400, 000], [400, 100], [400, 200], [400, 300], [400, 400], [400, 500], [400, 600], [400, 700], [400, 800], [400, 900], [400, 999],
#     [500, 000], [500, 100], [500, 200], [500, 300], [500, 400], [500, 500], [500, 600], [500, 700], [500, 800], [500, 900], [500, 999],
#     [600, 000], [600, 100], [600, 200], [600, 300], [600, 400], [600, 500], [600, 600], [600, 700], [600, 800], [600, 900], [600, 999],
#     [700, 000], [700, 100], [700, 200], [700, 300], [700, 400], [700, 500], [700, 600], [700, 700], [700, 800], [700, 900], [700, 999],
#     [800, 000], [800, 100], [800, 200], [800, 300], [800, 400], [800, 500], [800, 600], [800, 700], [800, 800], [800, 900], [800, 999],
#     [900, 000], [900, 100], [900, 200], [900, 300], [900, 400], [900, 500], [900, 600], [900, 700], [900, 800], [900, 900], [900, 999],
#     [999, 000], [999, 100], [999, 200], [999, 300], [999, 400], [999, 500], [999, 600], [999, 700], [999, 800], [999, 900], [999, 999],
# ]

# for point in points:
#     if point[0] > 0 and point[0] < 999:
#         xr = (np.random.randint(0,5) - 2) * 10
#         point[0] += xr
#     if point[1] > 0 and point[1] < 999:
#         yr = (np.random.randint(0,5) - 2) * 10
#         point[1] += yr
print(len(points))
size_on_line = 1
for point in points:
    if point[0] > 0 and point[0] < 999:
        xr = (numberData % 7 - 3) * 2
        numberData = numberData // 7
        point[0] += xr
        size_on_line *= 7
    if point[1] > 0 and point[1] < 999:
        yr = (numberData % 7 - 3) * 2
        numberData = numberData // 7
        point[1] += yr
        size_on_line *= 7
print('line: '+str((size_on_line.bit_length() + 7) // 8) + ' bytes')
# exit(0)
# 21 * 21 = 295 bytes + 1302 bytes = 1597
# 

print('FIRST STAGE')
print(str((numberData.bit_length() + 7) // 8) + ' bytes to next stage')

# preset points
# points = [[0, 0], [0, 110], [0, 180], [0, 300], [0, 410], [0, 480], [0, 620], [0, 680], [0, 800], [0, 890], [0, 999], [110, 0], [110, 110], [100, 190], [80, 310], [90, 420], [100, 510], [90, 610], [110, 720], [80, 810], [110, 910], [100, 999], [210, 0], [190, 110], [200, 200], [220, 280], [220, 410], [210, 480], [220, 610], [190, 700], [200, 820], [210, 910], [200, 999], [280, 0], [290, 80], [280, 220], [310, 290], [320, 380], [300, 490], [320, 580], [300, 710], [310, 810], [290, 920], [280, 999], [390, 0], [420, 100], [380, 190], [400, 290], [420, 420], [390, 510], [410, 610], [400, 720], [420, 800], [380, 900], [400, 999], [480, 0], [500, 90], [510, 190], [480, 300], [510, 420], [490, 480], [480, 600], [490, 720], [480, 790], [490, 920], [490, 999], [590, 0], [580, 110], [590, 190], [580, 310], [600, 400], [610, 490], [580, 600], [600, 700], [590, 780], [590, 890], [580, 999], [710, 0], [690, 100], [680, 200], [720, 320], [690, 400], [680, 500], [710, 600], [680, 710], [700, 800], [710, 890], [720, 999], [780, 0], [800, 120], [790, 220], [820, 320], [820, 380], [780, 500], [800, 590], [790, 720], [810, 820], [800, 880], [820, 999], [890, 0], [900, 120], [900, 210], [920, 280], [880, 420], [900, 520], [890, 620], [900, 700], [900, 810], [920, 900], [900, 999], [999, 0], [999, 90], [999, 220], [999, 290], [999, 410], [999, 490], [999, 610], [999, 680], [999, 810], [999, 880], [999, 999]]

point_creation_time = time.process_time() - start_time
delaunator = Delaunator(points)
triangles = delaunator.triangles
halfedges = delaunator.halfedges
hull = delaunator.hull
coords = delaunator.coords

# print("\npoints = "+str(points))
# print("\ncoords = "+str(coords))
# print("\ntriangles = "+str(triangles))
print(str(len(triangles)//3) + ' triangles')
# print("\nhalfedges = "+str(halfedges))
# print(str(len(halfedges)))
# print("\nhull = "+str(hull))
# print(str(len(hull)))

triangulation_time = time.process_time() - point_creation_time
print("\n" + str(point_creation_time))
print("\n" + str(triangulation_time))

## visualize
# generate image with white background
img = np.ones((maxSize, maxSize, 3), np.uint8) * 255
pointColor = (0,0,0)
triColor = [
    (0, 0, 255), (0, 255, 0), (255, 0, 0), 
    (0, 255, 255), (255, 255, 0), (255, 0, 255), 
    # (0, 128, 255), (0, 255, 128), (128, 255, 0), (255, 128, 0), (255, 0, 128), (128, 0, 255)
]
triColor = [
    (0, 0, 0), (0, 51, 0), (0, 102, 0), (0, 153, 0), (0, 204, 0), (0, 255, 0),
    (0, 0, 51), (0, 51, 51), (0, 102, 51), (0, 153, 51), (0, 204, 51), (0, 255, 51),
    (0, 0, 102), (0, 51, 102), (0, 102, 102), (0, 153, 102), (0, 204, 102), (0, 255, 102),
    (0, 0, 153), (0, 51, 153), (0, 102, 153), (0, 153, 153), (0, 204, 153), (0, 255, 153),
    (0, 0, 204), (0, 51, 204), (0, 102, 204), (0, 153, 204), (0, 204, 204), (0, 255, 204),
    (0, 0, 255), (0, 51, 255), (0, 102, 255), (0, 153, 255), (0, 204, 255), (0, 255, 255)
] # 36
edgeColor = (255, 255, 255)
hullColor = (192, 192, 0)
pointColor = (0, 0, 0)

# # draw point
# for i in range(len(points)):
#     p = np.array(points[i], dtype=np.int32)
#     print("\t" + str(p))
#     cv2.circle(img, (p[0], p[1]), 2, pointColor, thickness=2)

counts = []
for i in range(len(triColor)):
    counts.append(0)

# draw edge
size_on_color = 1
for i in range(len(triangles)//3):
    pointA = triangles[i*3]
    pointB = triangles[i*3+1]
    pointC = triangles[i*3+2]

    triangle_cnt = np.array( [(points[pointA][0], points[pointA][1]), (points[pointB][0], points[pointB][1]), (points[pointC][0], points[pointC][1])] )
    # print([triangle_cnt])
    # cv2.drawContours(img, [triangle_cnt], 0, triColor[i%len(triColor)], -1)
    # method 1: 51 (6)
    # cv2.drawContours(img, [triangle_cnt], 0, triColor[numberData%len(triColor)], -1)
    # counts[numberData%len(triColor)] += 1
    # numberData = numberData // len(triColor)
    # size_on_color *= len(triColor)

    # method 2: 15 (18)
    if numberData != 0:
        rgb = (numberData % 5830) + 1
        numberData = numberData // 5830
        r = rgb % 18
        g = (rgb // 18) % 18
        b = (rgb // 324) % 18 
        cv2.drawContours(img, [triangle_cnt], 0, (b*15, g*15, r*15), -1)
    else:
        r = np.random.randint(0,18)
        g = np.random.randint(0,18)
        b = np.random.randint(0,18)
        if excessData == 0:
            excessData = 1
        excessData *= 5832
        cv2.drawContours(img, [triangle_cnt], 0, (b*15, g*15, r*15), -1)
    size_on_color *= 5832

    # cv2.circle(img, (points[pointA][0], points[pointA][1]), 1, pointColor, 1, 8)
    # cv2.circle(img, (points[pointB][0], points[pointB][1]), 1, pointColor, 1, 8)
    # cv2.circle(img, (points[pointC][0], points[pointC][1]), 1, pointColor, 1, 8)
    # # line 1
    # start_point = (points[pointA][0], points[pointA][1])
    # end_point = (points[pointB][0], points[pointB][1])
    # cv2.line(img, start_point, end_point, edgeColor, 1)
    # # line 2
    # start_point = (points[pointB][0], points[pointB][1])
    # end_point = (points[pointC][0], points[pointC][1])
    # cv2.line(img, start_point, end_point, edgeColor, 1)
    # #line 3
    # start_point = (points[pointC][0], points[pointC][1])
    # end_point = (points[pointA][0], points[pointA][1])
    # cv2.line(img, start_point, end_point, edgeColor, 1)
    # print("\tTriangle " + str(i))
    # cv2.imshow("triangle", img)
    # cv2.waitKey(0)


print('color: '+str((size_on_color.bit_length() + 7) // 8) + ' bytes')
# cv2.imshow("triangle", img)
# cv2.waitKey(0)
print('Done')
# print(numberData.to_bytes((numberData.bit_length() + 7) // 8, 'little'))
# print((numberData.bit_length() + 7) // 8)
print(str((excessData.bit_length() + 7) // 8) + ' bytes')

# draw hull
# for i in range(len(hull) - 1):
#     pointA = hull[i]
#     pointB = hull[i+1]
#     # line 1
#     start_point = (points[pointA][0], points[pointA][1])
#     end_point = (points[pointB][0], points[pointB][1])
#     cv2.line(img, start_point, end_point, hullColor, 1)
# start_point = (points[hull[len(hull)-1]][0], points[hull[len(hull)-1]][1])
# end_point = (points[hull[0]][0], points[hull[0]][1])
# cv2.line(img, start_point, end_point, hullColor, 1)

# show image generated and save file
cv2.imshow("triangle", img)
cv2.waitKey(0)
cv2.imwrite('./testImage.jpg', img)

# for i in range(len(triColor)):
#     print(triColor[i])
#     print(counts[i])