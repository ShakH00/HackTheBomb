class base:
    def first(self):
        print("i am a base class")

class fderived(base):
    def second(self):
        print("i am first derived class")

class sderived(fderived):
    def third(self):
        print("I am second derived class")

obj=sderived()
obj.first()
obj.second()
obj.third()