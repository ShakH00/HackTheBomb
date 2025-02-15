"""
HYbrid inheritance doesn't support in python i am just trying but it didn't work
"""
class one:
    def first(self):
        print("i am first class")

class two:
    def second(self):
        print("i am second class")

class third:
    def three(self):
        print("i am third class")

class fourth(one,two,third):
    def four(self):
        print("i am fourth class")

obj=fourth()
obj.first()
obj.second()
obj.three()
obj.four()