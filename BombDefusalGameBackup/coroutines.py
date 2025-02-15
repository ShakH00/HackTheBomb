import time
#coroutine means all the line of function will not run again and again
def searcher():
    book="this is a book"
    time.sleep(3)
#above 2 line will run only first time after that you don't have to wait
    while True:
        text =(yield)
        if text in book:
            print("your text in a book")
        else:
            print("your text is not in a book")

s=searcher()
print("searching started...")
next(s)
s.send("book")
input("press any key")
s.send("Nitesh")
