import time
initial = time.time()
for i in range(45):
    print("hello world")
#print(time.time()-initial)
local= time.asctime(time.localtime(time.time()))
print(local)