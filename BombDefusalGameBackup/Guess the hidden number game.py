# Guess the hidden number game
# n=18
# while(1):
#     a=int(input("Guess the number\n"))
#     if n<a:
#         print("you're number is greater try again")
#         continue
#     elif n>a:
#         print("you're number is smaller try again")
#         continue
#     else:
#         print("you are absoultely right")
#         break

# Guess the hidden number game with 5 chances
n=18
print("you have 5 chances")
for i in range(0,5):
    a=int(input("Guess the number\n"))
    if n<a:
        print("you're number is greater try again")
        if i==4:
            print("Game over")
        else:
            continue
    elif n>a:
        print("you're number is smaller try again")
        if i==4:
            print("Game over")
        else:
            continue
    elif n==a:
        print("you are absoultely right\n")
        print("you win the game")
        if i==0:
            print("You completed game in One guess")
        elif i==1:
            print("You completed game in 2 guesses")
        elif i==2:
            print("You completed game in 3 guesses")
        elif i==3:
            print("You completed game in 4 guesses")
        else:
            print("You completed game in 5 guesses")