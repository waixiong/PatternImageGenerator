import time

tStart = time.perf_counter()

x = 0

for i in range(16 * 1024*1024) : 
    x += 256

print(x)

tEnd = time.perf_counter()

print(tEnd-tStart)