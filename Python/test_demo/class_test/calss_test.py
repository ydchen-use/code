import time


class Person:
    hair = "black"

    def __init__(self, name = "Charile", age = 8):
        self.name = name
        self.age = age

    def said(self):
        print("You said: ", self.name)

    def __said(self):
        print("Your age:", self.age)


if __name__ == "__main__":
    p = Person()
    p.said()
