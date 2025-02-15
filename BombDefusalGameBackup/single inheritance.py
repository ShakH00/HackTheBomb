class emp:
    def print(self):
        print("hello i am employee")

class programmer(emp):
    def print1(self):
        print("hello i am a programmer")

obj=programmer()
obj.print()
obj.print1()