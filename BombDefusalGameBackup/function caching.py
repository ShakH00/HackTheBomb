import time
from functools import lru_cache
#saving 3 second means only 3 second you have to wait for first time later it will not delay bcoz it already saved
@lru_cache(maxsize=3)
def work(n):
    time.sleep(n)
    return n

print("Now running")
#for delaying
work(3)
#it will delay more 69 second
work(6)
print("Done.. again calling")
work(3)
print("called again")