class helloworld:
    def fun1(self):
        print("hello world")

class student:
    pass

obj=helloworld()
obj1=helloworld()
obj2=student
obj2.name="Nitu"#instance variable
obj2.std="BCA"
obj2.place="Thane"
print(obj2.name,obj2.std,obj2.place)
obj.fun1()
obj1.fun1()
