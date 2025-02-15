class father:
    def first(self):
        print("i am base class")
class son(father):
    def second(self):
        print("i am son class or first derived class")

class grandson(father):
    def third(self):
        print("i am second derived class or grandson ")

obj=son()
obj1=grandson()
obj.first()
obj.second()
obj1.first()
obj1.third()