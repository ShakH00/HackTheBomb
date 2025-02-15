from abc import ABC,abstractmethod #importing abstract method
#this is abstract base class
class shape(ABC):
    @abstractmethod
    def printarea(self):
        return 0
class rectangle(shape):
    type ="rectangle"
    side = 4
    def __init__(self):
        self.length=6
        self.breadth=7
    def printarea(self):
        return self.length * self.breadth

obj = rectangle()
print(obj.printarea())