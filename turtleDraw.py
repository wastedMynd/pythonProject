import turtle
import math
import random

c = turtle.Turtle()
c.pencolor("black")
c.speed(100)
c.clear()


def star(t, size):
    if size <= 10:
        return
    else:
        t.forward(size / 2)
        t.left(217)
    pass


while True:
    for i in range(360):
        star(c, i)
        x = random.randint(0, 1)
        if i % 2 == 0:
            c.pencolor(["red","yellow"][x])
        else:
            c.pencolor(['orange','white'][x])

turtle.done()
