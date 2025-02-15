class add:
    def addition(self):
        a=int(input("Enter first number"))
        b = int(input("Enter second number"))
        c=a+b
        print("Addition of two number is ", c)

class sub:
    def substraction(self):
        a=int(input("Enter first number"))
        b = int(input("Enter second number"))
        c = a - b
        print("Substraction is ", c)

class cal(add,sub):
    def multiply(self):
        a = int(input("Enter first number"))
        b = int(input("Enter second number"))
        c = a * b
        print("multiplication is ", c)

obj=cal()
print("Enter 1 for addition")
print("Enter 2 for substraction")
print("Enter 3 for multiplication")
a=int(input())
if a==1:
    obj.addition()
elif a==2:
    obj.substraction()
elif a==3:
    obj.multiply()
else :
    print("Enter between 1 to 3")
