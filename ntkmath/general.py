class Curves:
    """
    A class for animating widget movements with different easing curves.

    This class provides various animation curves for moving widgets from one position
    to another with smooth transitions.
    """

    @staticmethod
    def linear(t: float) -> float:
        """
        Linear easing function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using linear easing
        """
        return t

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """
        Quadratic ease-in function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using quadratic ease-in
        """
        return t**2

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """
        Quadratic ease-out function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using quadratic ease-out
        """
        return t * (2 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """
        Quadratic ease-in-out function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using quadratic ease-in-out
        """
        return 2 * t * t if t < 0.5 else -1 + (4 - 2 * t) * t

    @staticmethod
    def ease_in_cubic(t: float) -> float:
        """
        Cubic ease-in function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using cubic ease-in
        """
        return t * t * t

    @staticmethod
    def ease_out_cubic(t: float) -> float:
        """
        Cubic ease-out function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using cubic ease-out
        """
        return (t - 1) * (t - 1) * (t - 1) + 1

    @staticmethod
    def bounce(t: float) -> float:
        """
        Bounce easing function.

        Args:
            t: A value between 0 and 1 representing animation progress

        Returns:
            The interpolated value using bounce easing
        """
        if t < (1 / 2.75):
            return 7.5625 * t * t
        elif t < (2 / 2.75):
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < (2.5 / 2.75):
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375


def clamp(number, minimum=0, maximum=0):
    """Implement clamp method

    Args:
        number (int): Number to clamp
        minimum (int, optional): Floor. Defaults to 0.
        maximum (int, optional): Ceiling. Defaults to 0.

    Returns:
        int: Clamped number
    """
    number = min(number, maximum)
    number = max(number, minimum)
    return number


def sign(x):
    """Return the sign of a number.

    Args:
        x (int/float): Number to get the sign of

    Returns:
        int: 1 for positive, -1 for negative
    """
    return (1, -1)[x < 0]
