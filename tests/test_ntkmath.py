import sys
import os

# Add the parent directory to the Python path so we can import ntkmath
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../ntkmath"))

import pytest
import math
import adv_decimal
import geometry
import general


class TestImports:
    """Test that all imports work correctly"""

    def test_import_general_functions(self):
        """Test that general utility functions can be imported"""
        assert callable(general.Curves.linear)
        assert callable(general.clamp)
        assert callable(general.sign)

    def test_import_geometry_classes(self):
        """Test that geometry classes can be imported"""
        assert geometry.Rectangle is not None
        assert geometry.Triangle is not None
        assert geometry.Angle is not None
        assert geometry.Point is not None
        assert geometry.Line is not None

    def test_import_decimal_classes(self):
        """Test that decimal arithmetic classes can be imported"""
        assert adv_decimal.FixedPointArithmetic is not None
        assert adv_decimal.FPT is not None
        assert adv_decimal.Decimal is not None
        # Test aliases
        assert adv_decimal.FPT is adv_decimal.FixedPointArithmetic
        assert adv_decimal.Decimal is adv_decimal.FixedPointArithmetic


class TestPoint:
    """Test the Point class"""

    def test_point_creation(self):
        """Test point creation"""
        p = geometry.Point(3, 4)
        assert p.x == 3
        assert p.y == 4

    def test_point_subscript_access(self):
        """Test that points support subscript access"""
        p = geometry.Point(5, 7)
        assert p[0] == 5
        assert p[1] == 7

        with pytest.raises(IndexError):
            _ = p[2]

    def test_point_iteration(self):
        """Test point iteration"""
        p = geometry.Point(1, 2)
        coords = list(p)
        assert coords == [1, 2]

    def test_point_offset(self):
        """Test point offset method"""
        p = geometry.Point(10, 20)
        new_p = p.offset(5, -3)
        assert new_p.x == 15
        assert new_p.y == 17
        # Original point should be unchanged
        assert p.x == 10
        assert p.y == 20

    def test_point_repr(self):
        """Test point string representation"""
        p = geometry.Point(1.5, 2.5)
        assert repr(p) == "Point(1.5, 2.5)"


class TestRectangle:
    """Test the Rectangle class"""

    def test_rectangle_creation(self):
        """Test rectangle creation with default values"""
        r = geometry.Rectangle()
        assert r.x == 0
        assert r.y == 0
        assert r.width == 0
        assert r.height == 0
        assert r.rotation == 0

    def test_rectangle_creation_with_values(self):
        """Test rectangle creation with specific values"""
        r = geometry.Rectangle(10, 20, 30, 40, 45)
        assert r.x == 10
        assert r.y == 20
        assert r.width == 30
        assert r.height == 40
        assert r.rotation == 45

    def test_rectangle_area(self):
        """Test rectangle area calculation"""
        r = geometry.Rectangle(0, 0, 10, 5)
        assert r.get_area() == 50

    def test_rectangle_points_no_rotation(self):
        """Test getting rectangle corner points without rotation"""
        r = geometry.Rectangle(0, 0, 10, 5, 0)
        a, b, c, d = r.get_points()

        # Check that points are Point objects
        assert isinstance(a, geometry.Point)
        assert isinstance(b, geometry.Point)
        assert isinstance(c, geometry.Point)
        assert isinstance(d, geometry.Point)

        # Check coordinates (approximately due to floating point)
        assert abs(a.x - 0) < 1e-10 and abs(a.y - 0) < 1e-10
        assert abs(b.x - 10) < 1e-10 and abs(b.y - 0) < 1e-10
        assert abs(c.x - 10) < 1e-10 and abs(c.y - 5) < 1e-10
        assert abs(d.x - 0) < 1e-10 and abs(d.y - 5) < 1e-10

    def test_rectangle_relative_point_no_rotation(self):
        """Test getting relative point in rectangle without rotation"""
        r = geometry.Rectangle(10, 10, 20, 20, 0)
        rel_x, rel_y = r.get_rel_point_rect(15, 15)
        assert rel_x == 5
        assert rel_y == 5

    def test_rectangle_point_inside_no_rotation(self):
        """Test point inside rectangle without rotation"""
        r = geometry.Rectangle(0, 0, 10, 10, 0)
        assert r.point_in_rectangle(5, 5) == True
        assert r.point_in_rectangle(15, 5) == False
        assert r.point_in_rectangle(5, 15) == False


class TestTriangle:
    """Test the Triangle class"""

    def test_triangle_creation(self):
        """Test triangle creation"""
        a = geometry.Point(0, 0)
        b = geometry.Point(3, 0)
        c = geometry.Point(0, 4)
        t = geometry.Triangle(a, b, c)

        assert t.a == a
        assert t.b == b
        assert t.c == c

    def test_triangle_area(self):
        """Test triangle area calculation"""
        # Right triangle with legs 3 and 4, area should be 6
        a = geometry.Point(0, 0)
        b = geometry.Point(3, 0)
        c = geometry.Point(0, 4)
        t = geometry.Triangle(a, b, c)

        area = t.get_area()
        assert abs(area - 6.0) < 1e-10


class TestAngle:
    """Test the Angle class"""

    def test_angle_normalize(self):
        """Test angle normalization"""
        assert geometry.Angle.normalize(0) == 0
        assert geometry.Angle.normalize(90) == 90
        assert geometry.Angle.normalize(360) == 0
        assert geometry.Angle.normalize(450) == 90
        assert geometry.Angle.normalize(-90) == 270
        assert geometry.Angle.normalize(-180) == 180

    def test_angle_to_radians(self):
        """Test angle conversion to radians"""
        assert abs(geometry.Angle.to_radians(0) - 0) < 1e-10
        assert abs(geometry.Angle.to_radians(90) - math.pi / 2) < 1e-10
        assert abs(geometry.Angle.to_radians(180) - math.pi) < 1e-10
        assert abs(geometry.Angle.to_radians(360) - 2 * math.pi) < 1e-10


class TestLine:
    """Test the Line function"""

    def test_line_creation(self):
        """Test line vector creation"""
        # 0 degrees, length 1
        line = geometry.Line(0, 1)
        assert isinstance(line, geometry.Point)
        assert abs(line.x - 1.0) < 1e-10
        assert abs(line.y - 0.0) < 1e-10

        # 90 degrees, length 1
        line = geometry.Line(math.pi / 2, 1)
        assert abs(line.x - 0.0) < 1e-10
        assert abs(line.y - 1.0) < 1e-10


class TestCurves:
    """Test the Curves class"""

    def test_linear_curve(self):
        """Test linear easing curve"""
        assert general.Curves.linear(0) == 0
        assert general.Curves.linear(0.5) == 0.5
        assert general.Curves.linear(1) == 1

    def test_ease_in_quad(self):
        """Test quadratic ease-in curve"""
        assert general.Curves.ease_in_quad(0) == 0
        assert general.Curves.ease_in_quad(0.5) == 0.25
        assert general.Curves.ease_in_quad(1) == 1

    def test_ease_out_quad(self):
        """Test quadratic ease-out curve"""
        assert general.Curves.ease_out_quad(0) == 0
        assert general.Curves.ease_out_quad(1) == 1
        # For t=0.5: t * (2 - t) = 0.5 * 1.5 = 0.75
        assert general.Curves.ease_out_quad(0.5) == 0.75

    def test_ease_in_out_quad(self):
        """Test quadratic ease-in-out curve"""
        assert general.Curves.ease_in_out_quad(0) == 0
        assert general.Curves.ease_in_out_quad(1) == 1
        # For t=0.25: 2 * 0.25 * 0.25 = 0.125
        assert general.Curves.ease_in_out_quad(0.25) == 0.125

    def test_ease_in_cubic(self):
        """Test cubic ease-in curve"""
        assert general.Curves.ease_in_cubic(0) == 0
        assert general.Curves.ease_in_cubic(0.5) == 0.125
        assert general.Curves.ease_in_cubic(1) == 1

    def test_ease_out_cubic(self):
        """Test cubic ease-out curve"""
        assert general.Curves.ease_out_cubic(0) == 0
        assert general.Curves.ease_out_cubic(1) == 1

    def test_bounce(self):
        """Test bounce easing curve"""
        assert general.Curves.bounce(0) == 0
        # Test that it returns reasonable values
        result = general.Curves.bounce(0.5)
        assert 0 <= result <= 1


class TestGeneralFunctions:
    """Test general utility functions"""

    def test_clamp(self):
        """Test clamp function"""
        assert general.clamp(5, 0, 10) == 5
        assert general.clamp(-5, 0, 10) == 0
        assert general.clamp(15, 0, 10) == 10
        assert general.clamp(5, 3, 7) == 5
        assert general.clamp(1, 3, 7) == 3
        assert general.clamp(10, 3, 7) == 7

    def test_sign(self):
        """Test sign function"""
        assert general.sign(5) == 1
        assert general.sign(-5) == -1
        assert general.sign(0) == 1  # Based on the implementation


class TestFixedPointArithmetic:
    """Test the FixedPointArithmetic class"""

    def test_fpa_creation(self):
        """Test FPA object creation"""
        fpa = adv_decimal.FixedPointArithmetic(10.5)
        assert fpa.number1 == 10.5
        assert fpa.precision == 23

    def test_fpa_addition(self):
        """Test FPA addition"""
        fpa = adv_decimal.FixedPointArithmetic(10.5)
        result = fpa + 5.5
        assert "16.0" in result or "16" in result

    def test_fpa_subtraction(self):
        """Test FPA subtraction"""
        fpa = adv_decimal.FixedPointArithmetic(10.5)
        result = fpa - 5.5
        assert "5.0" in result or "5" in result

    def test_fpa_multiplication(self):
        """Test FPA multiplication"""
        fpa = adv_decimal.FixedPointArithmetic(10)
        result = fpa * 2
        assert "20" in result

    def test_fpa_division(self):
        """Test FPA division"""
        fpa = adv_decimal.FixedPointArithmetic(10)
        result = fpa / 2
        assert "5" in result

    def test_fpa_comparison(self):
        """Test FPA comparison operations"""
        fpa1 = adv_decimal.FixedPointArithmetic(10)
        fpa2 = adv_decimal.FixedPointArithmetic(5)

        assert fpa1 > 5
        assert fpa1 >= 10
        assert fpa2 < 10
        assert fpa2 <= 5
        assert fpa1 == 10
        assert fpa1 != 5

    def test_fpa_generate_string_numbers(self):
        """Test the string number generation helper"""
        str1, str2, imp = adv_decimal.FixedPointArithmetic._generate_string_numbers(
            10.5, 5.25
        )
        assert str1 == "1050"
        assert str2 == "525"
        assert imp == 2

    def test_aliases(self):
        """Test that FPT and Decimal are aliases"""
        fpt = adv_decimal.FPT(10)
        decimal = adv_decimal.Decimal(10)

        assert isinstance(fpt, adv_decimal.FixedPointArithmetic)
        assert isinstance(decimal, adv_decimal.FixedPointArithmetic)


class TestIntegration:
    """Integration tests to ensure components work together"""

    def test_rectangle_with_triangle_area_calculation(self):
        """Test that rectangle point-in-rectangle uses triangle area correctly"""
        r = geometry.Rectangle(0, 0, 10, 10, 0)

        # Create a point that should be inside
        inside_point = geometry.Point(5, 5)
        assert r.point_in_rectangle(inside_point.x, inside_point.y) == True

        # Create a point that should be outside
        outside_point = geometry.Point(15, 15)
        assert r.point_in_rectangle(outside_point.x, outside_point.y) == False

    def test_point_in_triangle_calculations(self):
        """Test that triangles work correctly with point coordinates"""
        # Create triangle using points
        p1 = geometry.Point(0, 0)
        p2 = geometry.Point(4, 0)
        p3 = geometry.Point(2, 3)

        triangle = geometry.Triangle(p1, p2, p3)
        area = triangle.get_area()

        # Triangle with base 4 and height 3 should have area 6
        assert abs(area - 6.0) < 1e-10

    def test_angle_normalization_with_geometry(self):
        """Test angle normalization works with geometry calculations"""
        # Test with angles that need normalization
        angle_deg = 450  # Should normalize to 90
        normalized = geometry.Angle.normalize(angle_deg)
        assert normalized == 90

        # Convert to radians for use with geometry.Line
        angle_rad = geometry.Angle.to_radians(normalized)
        line = geometry.Line(angle_rad, 1)

        # Should be pointing up (y=1, x≈0)
        assert abs(line.x) < 1e-10
        assert abs(line.y - 1.0) < 1e-10


if __name__ == "__main__":
    pytest.main([__file__])
