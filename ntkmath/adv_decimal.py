class FixedPointArithmetic:
    """
    Fixed Point Arithmetic class for precise decimal calculations.

    This class provides arithmetic operations without floating-point precision issues
    by using string-based calculations.
    """

    def __init__(self, number1):
        self.number1 = number1
        self.precision = 23

    def _compensate(self, answer, imprecision):
        """Compensate for decimal precision in string representation."""
        answer_str = str(answer).replace(".", "")
        negative = answer_str[0] == "-"
        if answer_str[0] == "-":
            answer_str = answer_str[1:]
        if len(answer_str) <= imprecision:
            answer = "0." + "0" * (imprecision - len(answer_str)) + answer_str
        else:
            answer = f"{answer_str[:-imprecision]}.{answer_str[-imprecision:]}"
        return f"-{answer}" if negative else answer

    @staticmethod
    def _generate_string_numbers(number1, number2):
        """Convert nasty integers and floats into clean strings.

        Effectively ensures that both numbers are multiplied by the same number
        to get rid of the decimal.

        Args:
            number1 (str, int, float): First number
            number2 (str, int, float): Second number

        Returns:
            tuple: (string_number1, string_number2, imprecision)
        """

        def ensure_decimal(number):
            number_str = str(number)
            return number_str if "." in number_str else f"{number_str}.0"

        number1 = ensure_decimal(number1)
        number2 = ensure_decimal(number2)

        imprecision1 = len(number1.split(".")[1])
        imprecision2 = len(number2.split(".")[1])
        imprecision = max(imprecision1, imprecision2)

        def pad_zeros(number, imprecision, current_imprecision):
            return "".join(number.split(".")) + "0" * (
                imprecision - current_imprecision
            )

        string_number1 = pad_zeros(number1, imprecision, imprecision1)
        string_number2 = pad_zeros(number2, imprecision, imprecision2)

        return string_number1, string_number2, imprecision

    def __truediv__(self, number2, number1=None):
        """
        Divide with fixed-point precision.

        Args:
            number2 (str, int, float): Divisor
            number1 (str, int, float, optional): Dividend (uses self.number1 if None)

        Returns:
            str: String representation of the decimal result
        """

        if number1 is None:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                self.number1, number2
            )
        else:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                number1, number2
            )

        remainder = 0
        answer = ""
        negative = False
        if string_number2.startswith("-"):
            negative = not negative
        if string_number1.startswith("-"):
            negative = not negative

        string_number2 = int(string_number2.lstrip("-"))

        for i in string_number1.lstrip("-"):
            remainder += int(i)
            answer += str(remainder // string_number2)
            remainder %= string_number2
            remainder *= 10
        answer += "."
        for _ in range(self.precision):
            answer += str(remainder // string_number2)
            remainder = remainder % string_number2
            remainder *= 10
            if remainder == 0:
                break

        return "-" + answer.lstrip("0") if negative else answer.lstrip("0")

    def __rtruediv__(self, number2):
        return self.__truediv__(self.number1, number2)

    def __add__(self, number2):
        """Addition with fixed-point precision.

        Args:
            number2 (str, int, float): Number to add

        Returns:
            str: String representation of the decimal result
        """
        string_number1, string_number2, imprecision = self._generate_string_numbers(
            self.number1, number2
        )
        answer = int(string_number1) + int(string_number2)
        # Compensate
        answer = self._compensate(answer, imprecision)
        return answer

    def __radd__(self, number2):
        return self.__add__(number2)

    def __sub__(self, number2, number1=None):
        """Subtraction with fixed-point precision.

        Args:
            number2 (str, int, float): Number to subtract
            number1 (str, int, float, optional): Base number (uses self.number1 if None)

        Returns:
            str: String representation of the decimal result
        """
        if number1 is None:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                self.number1, number2
            )
        else:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                number1, number2
            )
        answer = int(string_number1) - int(string_number2)
        # Compensate
        answer = self._compensate(answer, imprecision)
        return answer

    def __rsub__(self, number2):
        return self.__sub__(self.number1, number2)

    def __mul__(self, number2):
        """Multiplication with fixed-point precision.

        Args:
            number2 (str, int, float): Number to multiply

        Returns:
            str: String representation of the decimal result
        """
        string_number1, string_number2, imprecision = self._generate_string_numbers(
            self.number1, number2
        )
        answer = int(string_number1) * int(string_number2)
        # Compensate
        answer = self._compensate(answer, imprecision * 2).rstrip("0")
        if answer.endswith("."):
            answer += "0"
        return answer

    def __rmul__(self, number2):
        return self.__mul__(number2)

    def __le__(self, number2, number1=None):
        if number1 is None:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                self.number1, number2
            )
        else:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                number1, number2
            )
        answer = int(string_number1) <= int(string_number2)
        return answer

    def __rle__(self, number2):
        return self.__le__(self.number1, number2)

    def __ge__(self, number2, number1=None):
        if number1 is None:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                self.number1, number2
            )
        else:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                number1, number2
            )
        answer = int(string_number1) >= int(string_number2)
        return answer

    def __rge__(self, number2):
        return self.__ge__(self.number1, number2)

    def __lt__(self, number2, number1=None):
        if number1 is None:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                self.number1, number2
            )
        else:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                number1, number2
            )
        answer = int(string_number1) < int(string_number2)
        return answer

    def __rlt__(self, number2):
        return self.__lt__(self.number1, number2)

    def __gt__(self, number2, number1=None):
        if number1 is None:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                self.number1, number2
            )
        else:
            string_number1, string_number2, imprecision = self._generate_string_numbers(
                number1, number2
            )
        answer = int(string_number1) > int(string_number2)
        return answer

    def __rgt__(self, number2):
        return self.__gt__(self.number1, number2)

    def __eq__(self, number2):
        string_number1, string_number2, imprecision = self._generate_string_numbers(
            self.number1, number2
        )
        answer = int(string_number1) == int(string_number2)
        return answer

    def __req__(self, number2):
        return self.__eq__(self.number1, number2)

    def __ne__(self, number2):
        return not self.__eq__(number2)

    def __rne__(self, number2):
        return not self.__eq__(self.number1, number2)


# Alias for backward compatibility
FPT = FixedPointArithmetic
Decimal = FixedPointArithmetic
