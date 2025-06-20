# Subscriptable point class
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0, rotation=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation

    def point_in_rectangle(self, x, y):
        pass


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c


# Static class
class Angle:
    pass


def Line(angle, length):
    """Return a point from the end of a line from angle and length."""
    pass
