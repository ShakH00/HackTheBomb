"""
Alternative constructor is that type of constructor who take agruement as a string
And split that string into that class type variable and assign to it.
Class method as alternative constructor.
"""
class Emp:
    def __init__(self,n,s,r):
        self.name=n
        self.salary=s
        self.role=r
        print(self.name,self.salary,self.role)
#this class method use for alternative constructor
    @classmethod #decorator
    def from_str(cls,s):
        #converting string into list
        p= s.split("-")
        return cls(p[0],p[1],p[2])
#Static method just a method if any time we want to use a function but not everytime
#its give speed and accuracy
    @staticmethod #decorator
    def good(string):
        print("this is " +string)

obj1=Emp("nitu",95000,"Student")
obj=Emp.from_str("Nitesh-480-teacher")
obj.good("Nitesh")