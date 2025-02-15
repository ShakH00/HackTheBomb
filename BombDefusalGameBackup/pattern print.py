n=int(input("Enter the rows"))
# m=bool(input("enter the number one or zero"))
# if(m==1):
for i in range(n):
    for j in range(i):
        print("*",end="")
    print('')
