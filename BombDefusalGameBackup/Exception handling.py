print("Enter num 1")
num1 = input()
print("Enter num 2")
num2 = input()
# Even input is not interger but we want to excute important line for that we use try and except keyword or exception handling
try:
    print("The sum of these two numbers is",
          int(num1)+int(num2))
except Exception as e:
    print(e)

finally:
    print("Run anyway...")

# imp line
print("This line is very important")

