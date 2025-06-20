from math import sin, asin, cos, radians, sqrt

try:
    from .general import sign
except ImportError:
    from general import sign


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def offset(self, offset_x, offset_y):
        """Offset a point by given amounts.

        Args:
            point (tuple): (x, y) coordinates of the point
            offset_x (float): X offset
            offset_y (float): Y offset

        Returns:
            tuple: (x, y) coordinates of the offset point
        """
        return Point(self.x + offset_x, self.y + offset_y)

    def __iter__(self):
        return iter((self.x, self.y))

    def __getitem__(self, index):
        """Support subscript access: point[0] = x, point[1] = y"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Point index out of range (0-1)")

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Rectangle:
    def __init__(self, x=0, y=0, width=0, height=0, rotation=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation

    def get_area(self):
        """Get the area of the rectangle."""
        return self.width * self.height

    def get_points(self):
        """Get 4 corner points of a rectangle, accounting for rotation.

        Returns:
            tuple: Four Point objects representing the corners (a, b, c, d)
                  where a is origin, b is origin+width, c is opposite corner, d is origin+height
        """
        # Starting point (origin)
        a = Point(self.x, self.y)

        # Convert rotation to radians
        rad_angle = radians(Angle.normalize(self.rotation))

        # Width vector (along rotation angle)
        width_vector = Line(rad_angle, self.width)
        b = a.offset(width_vector.x, width_vector.y)

        # Height vector (perpendicular to width, 90 degrees rotated)
        height_angle = rad_angle + radians(90)  # Add 90 degrees for perpendicular
        height_vector = Line(height_angle, self.height)
        d = a.offset(height_vector.x, height_vector.y)

        # Opposite corner (origin + width + height)
        c = d.offset(width_vector.x, width_vector.y)

        return a, b, c, d

    def get_rel_point_rect(self, x, y):
        """Get relative point in a rectangle given absolute coordinates, compensating for rotation.

        Args:
            x (float): Absolute x coordinate
            y (float): Absolute y coordinate

        Returns:
            tuple: (x, y) relative coordinates within the rectangle (0-width, 0-height range)
        """
        # Translate point to rectangle's origin
        dx = x - self.x
        dy = y - self.y

        # If no rotation, return simple translation
        if self.rotation == 0:
            return dx, dy

        # Apply inverse rotation to get relative coordinates
        rad_angle = radians(Angle.normalize(self.rotation))
        cos_a = cos(-rad_angle)  # Negative angle for inverse rotation
        sin_a = sin(-rad_angle)

        # Apply 2D rotation matrix (inverse rotation)
        rel_x = dx * cos_a - dy * sin_a
        rel_y = dx * sin_a + dy * cos_a

        return rel_x, rel_y

    def point_in_rectangle(self, x, y):
        """Check if a point is inside a rectangle's bounds, accounting for rotation.

        Args:
            rect_obj: Rectangle object with position, size, and rotation
            x (float): X coordinate of the point
            y (float): Y coordinate of the point

        Returns:
            bool: True if point is inside the rectangle
        """
        hit = (int(x), int(y))
        a, b, c, d = self.get_points()

        rect_area = self.get_area()

        area_apd = Triangle(a, hit, d).get_area()
        area_dpc = Triangle(d, hit, c).get_area()
        area_cpb = Triangle(c, hit, b).get_area()
        area_pba = Triangle(hit, b, a).get_area()

        # If the sum of the areas of the triangles equals the rectangle area, the point is inside
        return sum((area_apd, area_dpc, area_cpb, area_pba)) <= rect_area


class Triangle:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def get_area(self):
        """Get the area of a triangle given 3 points.

        Returns:
            float: Area of the triangle
        """
        return (
            abs(
                (self.b[0] * self.a[1] - self.a[0] * self.b[1])
                + (
                    self.c[0] * self.b[1]
                    - self.b[0] * self.c[1]
                    + self.a[0] * self.c[1]
                    - self.c[0] * self.a[1]
                )
            )
            / 2
        )


class Angle:
    @staticmethod
    def normalize(angle):
        """Normalize angle to be within [0, 360) degrees."""
        return (360 + angle) % 360

    @staticmethod
    def to_radians(degrees):
        """Convert angle to radians."""
        return radians(degrees)


def Line(angle, length):
    """Create a line vector from angle and length.

    Args:
        angle (float): Angle in radians
        length (float): Length of the vector

    Returns:
        Point: Vector as a Point with x,y components
    """
    x = length * cos(angle)
    y = length * sin(angle)
    return Point(x, y)
