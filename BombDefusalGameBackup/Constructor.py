"""
constructor
And constructor declare with init build-in function and always have parameter
"""
class Emp:
    #def __init__(self):
        #self.g="hello world"
       # print("hello world")
    def __init__(self,n,s,r):
        self.name=n
        self.salary=s
        self.role=r
        print(self.name,self.salary,self.role)

#obj=Emp()
obj1=Emp("nitu",95000,"Student")