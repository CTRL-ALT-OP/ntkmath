"""
Example usage of the ntkmath package.

This demonstrates how to import and use functions and classes
directly from the ntkmath package.
"""

# Import directly from ntkmath - this is what you wanted!
from ntkmath import (
    solve_quadratic,
    LinearEquation,  # Algebra
    Point,
    Circle,
    distance,  # Geometry
    mean,
    median,
    mode,
    std_dev,  # Statistics
)


def main():
    print("=== ntkmath Package Demo ===\n")

    # Algebra examples
    print("🔢 ALGEBRA:")
    print("-" * 20)

    # Quadratic equation: x² - 5x + 6 = 0
    x1, x2 = solve_quadratic(1, -5, 6)
    print(f"solve_quadratic(1, -5, 6) = {x1}, {x2}")

    # Linear equation: 2x - 6 = 0
    eq = LinearEquation(2, -6)
    print(f"LinearEquation(2, -6).solve() = {eq.solve()}")
    print(f"Equation: {eq}")
    print()

    # Geometry examples
    print("📐 GEOMETRY:")
    print("-" * 20)

    # Points and distance
    p1 = Point(1, 2)
    p2 = Point(4, 6)
    print(f"Point 1: {p1}")
    print(f"Point 2: {p2}")
    print(f"Distance between points: {p1.distance_to(p2):.2f}")
    print(f"Using distance function: {distance(1, 2, 4, 6):.2f}")

    # Circle
    circle = Circle(Point(0, 0), 5)
    print(f"Circle: {circle}")
    print(f"Area: {circle.area():.2f}")
    print(f"Circumference: {circle.circumference():.2f}")
    print(f"Contains Point(3, 4): {circle.contains_point(Point(3, 4))}")
    print()

    # Statistics examples
    print("📊 STATISTICS:")
    print("-" * 20)

    data = [1, 2, 2, 3, 4, 4, 4, 5, 6]
    print(f"Data: {data}")
    print(f"Mean: {mean(data):.2f}")
    print(f"Median: {median(data):.2f}")
    print(f"Mode: {mode(data)}")
    print(f"Standard deviation: {std_dev(data):.2f}")
    print()

    print("✅ All imports worked! You can now use:")
    print("   from ntkmath import solve_quadratic, Point, mean, ...")


if __name__ == "__main__":
    main()
