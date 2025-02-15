class A:
    def __int__(self):
        print("I am inside class A")

class B(A):
    def __int__(self):
        super().__int__()#super keyword handle overridding of constructor without super keyword
                         #we can't access class A constructor
        print("i am in class B")

obj=A()
obj1=B()
#obj.__int__()
obj1.__int__()
