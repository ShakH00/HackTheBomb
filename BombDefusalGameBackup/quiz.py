#
# while(1):
#       a = int(input("enter a number\n"))
#       if a>100:
#             print("you entered above 100")
#             break
#       else:
#             print("try again")
#             continue
# while(True):
#     inp = int(input("Enter a Number\n"))
#     if inp>100:
#         print("Congrats you have entered a number greater than 100\n")
#         break
#     else:
#         print("Try again!\n")
#         continue
# ================================================
# faulty calulator
a = int(input("Enter first number\n"))
c = input("enter operator +,-,*,/\n")
b = int(input("enter second number\n"))
if a==45 and b==3 and c=="*":
      print("555")
elif a==56 and b==9 and c=="+":
      print("77")
elif a==56 and b==6 and c=="/":
      print("4")
elif c== "+":
      d = a+b
      print(d)
elif c == "-":
      d=a-b
      print(d)
elif c=="*":
      d=a*b
      print(d)
elif c=="/":
      d=a/b
      print(d)
else:
      print("enter correct opertor")
