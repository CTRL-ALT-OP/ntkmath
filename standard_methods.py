from math import sin, asin, cos, radians, sqrt

# Define the names of objects
IMAGE_OBJECTS = [
    "image_object",
    "active_object",
    "hover_object",
    "hover_object_active",
]

BG_OBJECTS = ["bg_object", "bg_object_active"]

TEXT_OBJECTS = [
    "text_object",
    "active_text_object",
]

SLIDER_OBJECTS = ["slider_object", "slider_bg_object"]

ALL_OBJECTS = IMAGE_OBJECTS + BG_OBJECTS + TEXT_OBJECTS  # + SLIDER_OBJECTS


class FPT:
    def __init__(self, number1):
        self.number1 = number1
        self.precision = 23

    def _compensate(self, answer, imprecision):
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
        """Convert nasty integers and floats into clean strings. Effectively ensures that both numbers are multiplied by the same number to get rid of the decimal.

        Args:
            number1 (str, int, float): Numero uno
            number2 (str, int, float): Numero dos
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
        Divide
        Division sucks
        Lets reinvent it because we can

        Args:
            dividend (str, int, float): _description_
            divisor (str, int, float): _description_
            precision (int, optional): _description_. Defaults to 23.

        Returns:
            str: String representation of the decimal result. We hate floats.
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
        """Addtion but now with more steps because floatsssss

        Args:
            number1 (str, int, float): Numero uno
            number2 (str, int, float): Numero dos

        Returns:
            str: String representation of the decimal result. We hate floats.
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
        """Subtraction but now with more steps because floatsssss

        Args:
            number1 (str, int, float): Numero uno
            number2 (str, int, float): Numero dos

        Returns:
            str: String representation of the decimal result. We hate floats.
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
        """Multiplication but now with more steps because floatsssss

        Args:
            number2 (str, int, float): Numero dos

        Returns:
            str: String representation of the decimal result. We hate floats.
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


def check(_object, attribute):
    """Check if the given attribute is defined and is not None.

    Args:
        _object (nebulatk.Widget): widget
        attribute (str): attribute

    Returns:
        bool: Returns True if both checks are satisfied, False otherwise
    """
    return bool(hasattr(_object, attribute) and getattr(_object, attribute) is not None)


# Unfortunately not included in the python math library
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
    return (1, -1)[x < 0]


def rel_position_to_abs(_object, x, y):
    # Add up positions for relative offsets in parent tree
    obj = _object
    while hasattr(obj, "root") and hasattr(obj, "master") and obj.root != obj.master:
        # Safety check: only add position if root has x and y attributes
        if hasattr(obj.root, "x") and hasattr(obj.root, "y"):
            x += obj.root.x
            y += obj.root.y
        obj = obj.root
    return x, y


def abs_position_to_rel(_object, x, y):
    # Add up positions for relative offsets in parent tree
    obj = _object
    while hasattr(obj, "root") and hasattr(obj, "master") and obj.root != obj.master:
        # Safety check: only subtract position if root has x and y attributes
        if hasattr(obj.root, "x") and hasattr(obj.root, "y"):
            x -= obj.root.x
            y -= obj.root.y
        obj = obj.root
    return x, y


def get_line_point_rel(angle, length):
    bx = length * sin(angle)
    by = length * cos(angle)
    return bx, by


def offset_point(a, _a, _b):
    bx = a[0] + _b
    by = a[1] + _a
    return bx, by


def normalize_angle(angle):
    return (360 + angle) % 360


def get_rect_points(_object):
    """Gets 4 points of a rectangle, given the object's position and orientation"""

    # Add up positions for relative offsets in parent tree
    x = _object.x
    y = _object.y
    obj = _object
    while hasattr(obj, "root") and hasattr(obj, "master") and obj.root != obj.master:
        # Safety check: only add position if root has x and y attributes
        if hasattr(obj.root, "x") and hasattr(obj.root, "y"):
            x += obj.root.x
            y += obj.root.y
        obj = obj.root

    a = (x, y)

    # Normalize angle to be within [0, 360)
    angle = normalize_angle(_object.orientation)

    # Convert angle to radians for trigonometric functions
    rad_angle = radians(angle)

    _a, _b = get_line_point_rel(rad_angle, _object.width)

    b = offset_point(a, _a, _b)

    _a2, _b2 = get_line_point_rel(rad_angle, _object.height)

    d = offset_point(a, _b2, -_a2)

    c = offset_point(d, _a, _b)

    return a, b, c, d


def get_rel_point_rect(_object, x, y):
    """Returns the relative point in a rectangle given a pair of absolute coordinates, and compensating for rotation"""
    a = rel_position_to_abs(_object, _object.x, _object.y)
    a1 = y - a[1]
    b1 = x - a[0]
    signs = (sign(b1), sign(a1))
    c = sqrt(pow(a1, 2) + pow(b1, 2))
    if c == 0:
        return 0, 0
    B = asin(a1 / c)
    A = radians(normalize_angle(_object.orientation))

    A2 = A - B

    bx = c * signs[0] * abs(cos(A2))
    by = c * signs[1] * abs(sin(A2))

    return int(round(bx)), int(round(by))


def get_rect_area(_object):
    return _object.width * _object.height


def get_triangle_area(a, b, c):
    """Gets the area of a triangle, given 3 points"""
    return (
        abs(
            (b[0] * a[1] - a[0] * b[1])
            + (c[0] * b[1] - b[0] * c[1] + a[0] * c[1] - c[0] * a[1])
        )
        / 2
    )


def check_hit(_object, x, y):
    """Checks if a point is inside a given object's rectangular bounds approximation"""
    if not _object.initialized:
        return False
    if not _object.visible:
        return False

    if not _object.can_focus:
        return False

    hit = (int(x), int(y))
    a, b, c, d = get_rect_points(_object)

    rect_area = get_rect_area(_object)

    area_apd = get_triangle_area(a, hit, d)
    area_dpc = get_triangle_area(d, hit, c)
    area_cpb = get_triangle_area(c, hit, b)
    area_pba = get_triangle_area(hit, b, a)

    # If the sum of the areas of the triangles apd, dpc, cpb, and pba are less than or equal to the rectangle area, we are inside it.
    # Generally on a hit, the sum of the area of the triangles should always be equal to the area of the triangles
    if sum((area_apd, area_dpc, area_cpb, area_pba)) <= rect_area:
        if _object.bounds_type != "non-standard":
            return True
        x, y = get_rel_point_rect(_object, x, y)
        if y not in _object.bounds:
            return False

        for bounds in _object.bounds[y]:
            if bounds[0] <= x and bounds[1] >= x:
                return True
    return False


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


# ============================================================ FLOPS ======================================================================
# NOTE: Flops hide all items of a type, and shows the selected item


def image_flop(_object, val):
    """Hides all images, and shows the selected image

    Args:
        _object (nebulatk.Widget): widget
        val (str): Item to show
    """
    visible = "normal" if _object.visible else "hidden"
    if check(_object, val):
        for obj in IMAGE_OBJECTS:
            if hasattr(_object, obj):
                if val == obj:
                    _object.master.change_state(getattr(_object, obj), state=visible)
                else:
                    _object.master.change_state(getattr(_object, obj), state="hidden")


def bg_flop(_object, val):
    """Hides all background objects, and shows the selected background object

    Args:
        _object (nebulatk.Widget): widget
        val (str): Item to show
    """
    visible = "normal" if _object.visible else "hidden"
    for obj in BG_OBJECTS:
        if check(_object, obj):
            if val == obj:
                _object.master.change_state(getattr(_object, obj), state=visible)
            else:
                _object.master.change_state(getattr(_object, obj), state="hidden")


def text_flop(_object, val):
    """Hides all text objects, and shows the selected text object

    Args:
        _object (nebulatk.Widget): widget
        val (str): Item to show
    """
    visible = "normal" if _object.visible else "hidden"
    if hasattr(_object, val) and getattr(_object, val) is not None:
        for obj in TEXT_OBJECTS:
            if hasattr(_object, obj):
                if val == obj:
                    _object.master.change_state(getattr(_object, obj), state=visible)
                else:
                    _object.master.change_state(getattr(_object, obj), state="hidden")


def flop_off(_object):
    """Hides all objects

    Args:
        _object (nebulatk.Widget): widget
    """
    for obj in ALL_OBJECTS:
        if hasattr(_object, obj):
            _object.master.change_state(getattr(_object, obj), state="hidden")


def flop_on(_object):
    """Shows all objects

    Args:
        _object (nebulatk.Widget): widget
    """
    # visible = "normal" if _object.visible else "hidden"
    if _object.state:
        if _object.hovering:
            image_flop(_object, "hover_object_active")
        else:
            image_flop(_object, "active_object")
    elif _object.hovering:
        image_flop(_object, "hover_object")
    else:
        image_flop(_object, "image_object")
    if _object.bg_object_active is not None and _object.state:
        bg_flop(_object, "bg_object_active")

    else:
        bg_flop(_object, "bg_object")

    if _object.active_text_object is not None and _object.state:
        text_flop(_object, "active_text_object")
    else:
        text_flop(_object, "text_object")

    # _object.master.change_state(_object.slider_bg_object, visible)


# ============================================================ STANDARD WIDGET MANAGMENT METHODS ==========================================


# ------------------------------------------------------------ DELETION BEHAVIOUR -----------------------------------------------------------


def delete(_object, delayed=False):
    """Widget deletion behaviour

    Args:
        _object (nebulatk.Widget): widget
    """
    # Iterate through all items in the widget and delete them if they exist
    if delayed and _object._scheduled_deletion != []:
        for obj in _object._scheduled_deletion:
            _object.master.delete(obj)
        _object._scheduled_deletion = []
        return

    for obj in ALL_OBJECTS:
        if check(_object, obj):
            if delayed:
                _object._scheduled_deletion.append(getattr(_object, obj))
            else:
                _object.master.delete(getattr(_object, obj))
            setattr(_object, obj, None)


# ------------------------------------------------------------ DELETION SCHEDULING BEHAVIOUR -----------------------------------------------
def schedule_delete(_object):
    for obj in ALL_OBJECTS:
        if check(_object, obj):
            _object._scheduled_deletion.append(getattr(_object, obj))
            setattr(_object, obj, None)


def delete_scheduled(_object):
    for obj in _object._scheduled_deletion:
        _object.master.delete(obj)
    _object._scheduled_deletion = []


# ------------------------------------------------------------ HOVERING BEHAVIOUR -----------------------------------------------------------


def hovered_standard(_object):
    """Widget hover behaviour for standard type widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    if _object.visible:
        image_flop(_object, "hover_object")
        if _object.bg_object_active is not None:
            bg_flop(_object, "bg_object_active")
        if _object.active_text_object is not None:
            text_flop(_object, "active_text_object")


def hovered_toggle(_object):
    """Widget hover behaviour for toggle type widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    if _object.visible:
        if _object.state:
            image_flop(_object, "hover_object_active")
        else:
            image_flop(_object, "hover_object")


def hover_end(_object):
    """Widget hover end behaviour for all widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    if _object.visible:
        if _object.state:
            image_flop(_object, "active_object")
        else:
            image_flop(_object, "image_object")
            if _object.active_text_object is not None:
                text_flop(_object, "text_object")
        if _object.bg_object_active is not None:
            bg_flop(_object, "bg_object")


# ------------------------------------------------------------ TOGGLE BEHAVIOUR -------------------------------------------------------------


def toggle_object_standard(_object):
    """Widget toggle behaviour for standard type widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    _object.state = not _object.state
    if _object.hovering:
        image_flop(_object, "hover_object_active")
    else:
        image_flop(_object, "active_object")


def toggle_object_toggle(_object):
    """Widget toggle behaviour for toggle type widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    _object.state = not _object.state
    if _object.state:
        if _object.hovering:
            image_flop(_object, "hover_object_active")
        else:
            image_flop(_object, "active_object")

    elif _object.hovering:
        image_flop(_object, "hover_object")
    else:
        image_flop(_object, "image_object")
    if check(_object, "bg_object_active"):
        if not _object.state:
            bg_flop(_object, "bg_object")

        else:
            bg_flop(_object, "bg_object_active")

    if check(_object, "active_text_object"):
        if not _object.state:
            text_flop(_object, "text_object")

        else:
            text_flop(_object, "active_text_object")


# ------------------------------------------------------------ CLICK BEHAVIOUR --------------------------------------------------------------


def clicked_standard(_object):
    """Widget click behaviour for standard type widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    if _object.visible:
        toggle_object_standard(_object)
        if _object.command is not None:
            _object.command()


def clicked_toggle(_object):
    """Widget click behaviour for toggle type widgets

    Args:
        _object (nebulatk.Widget): widget
    """
    if _object.visible:
        toggle_object_toggle(_object)

        if _object.command is not None and _object.state:
            _object.command()
        if _object.command_off is not None and not _object.state:
            _object.command_off()
        elif _object.command is not None and not _object.state:
            _object.command()


# ------------------------------------------------------------ POSITION BEHAVIOURS ----------------------------------------------------------


def _update_position(_object, item, x, y, old_x, old_y):
    """Internal update_position method

    Args:
        _object (nebulatk.Widget): widget
        item (str): item
        x (int): x position
        y (int): y position
    """
    if check(_object, item):
        if item.find("image") != -1:
            x += _object.border_width / 2
            y += _object.border_width / 2
        elif item.find("text") != -1:
            if _object.justify == "center":
                x = x + (_object.width / 2)

            elif _object.justify == "left":
                x = x

            elif _object.justify == "right":
                x = x + _object.width

            # Set y offset
            y = y + (_object.height / 2)
        _object.master.object_place(getattr(_object, item), x, y)


def update_positions(_object, x, y, avoid_slider=False):
    """Update positions of all objects

    Args:
        _object (nebulatk.Widget): widget
        x (int): x position
        y (int): y position
        avoid_slider (bool, optional): Request to avoid touching the slider background objects. Defaults to False.
    """
    x, y = rel_position_to_abs(_object, x, y)
    old_x, old_y = rel_position_to_abs(_object, _object.x, _object.y)

    for obj in ALL_OBJECTS:
        if obj == "slider_bg_object" and avoid_slider:
            continue
        _update_position(_object, obj, x, y, old_x, old_y)


# ------------------------------------------------------------ PLACEMENT BEHAVIOURS ---------------------------------------------------------


def place_bulk(_object, x, y):
    """Bulk place objects

    Args:
        _object (nebulatk.Widget): widget
    """
    x, y = rel_position_to_abs(_object, x, y)
    # Only place background rectangles if there == a fill or border
    # Place slider_bg_object
    # colors = _object._colors
    state = "normal" if _object.visible else "hidden"
    """if colors["slider_fill"] is not None or (
        colors["slider_border"] is not None and _object.slider_border_width != 0
    ):
        _object.slider_bg_object = _object.master.create_rectangle(
            x,
            y + _object.height / 2 - _object.slider_height / 2,
            x + _object.maximum + _object.width,
            y + _object.height / 2 - _object.slider_height / 2 + _object.slider_height,
            fill=_object.slider_fill,
            border_width=_object.slider_border_width,
            outline=_object.slider_border,
            state=state,
        )"""
    # Place bg_object
    if _object.fill is not None or (
        _object.border is not None and _object.border_width != 0
    ):
        _object.bg_object, img = _object.master.create_rectangle(
            x,
            y,
            x + _object.width,
            y + _object.height,
            fill=_object.fill,
            border_width=_object.border_width,
            outline=_object.border,
            state=state,
        )
        _object._images_initialized["bg_object"] = img

    # Place bg_object_active
    if _object.active_fill is not None:
        _object.bg_object_active, img = _object.master.create_rectangle(
            x,
            y,
            x + _object.width,
            y + _object.height,
            fill=_object.active_fill,
            border_width=_object.border_width,
            outline=_object.border,
            state="hidden",
        )
        _object._images_initialized["bg_object_active"] = img

    # Place images
    for img in ["image", "active_image", "hover_image", "active_hover_image"]:
        if check(_object, img):
            state = "hidden"
            img_object = img.split("_")[0] + "_object"
            if img == "image" and _object.visible:
                state = "normal"
            if img == "active_hover_image":
                img_object = "hover_object_active"

            id, image = _object.master.create_image(
                x + _object.border_width,
                y + _object.border_width,
                getattr(_object, img),
                state=state,
            )
            setattr(
                _object,
                img_object,
                id,
            )
            _object._images_initialized[img] = image

    # Place text objects
    if _object.text != "":
        generate_text(_object, x, y)


def generate_text(_object, x, y):
    state = "normal" if _object.visible else "hidden"
    # Set x offset and anchor based on justify
    if _object.justify == "center":
        local_x = x + (_object.width / 2)
        anchor = "center"

    elif _object.justify == "left":
        local_x = x
        anchor = "w"

    elif _object.justify == "right":
        local_x = x + _object.width
        anchor = "e"

    # Set y offset
    local_y = y + (_object.height / 2)

    _object.text_object, img = _object.master.create_text(
        local_x,
        local_y,
        text=_object.text,
        font=_object.font,
        fill=_object.text_color,
        anchor=anchor,
        state=state,
        angle=_object.orientation,
    )
    if _object.active_text_color is not None:
        _object.active_text_object, img = _object.master.create_text(
            local_x,
            local_y,
            text=_object.text,
            font=_object.font,
            fill=_object.active_text_color,
            anchor=anchor,
            state="hidden",
        )


from PIL import Image as pil
from PIL import ImageTk as piltk
from PIL import ImageDraw as pildraw

import math

try:
    from . import standard_methods
    from . import colors_manager
except ImportError:
    import standard_methods
    import colors_manager


class Image:
    def __init__(self, image, _object=None):
        self.image = None
        self.tk_images = {}
        self.bounds = []

        if type(image) is Image:
            self.image = image.image

            if _object is not None:
                # Resize image if size isn't specified
                if _object.width != 0 and _object.height != 0:
                    self.resize(
                        _object.width - (_object.border_width * 2),
                        _object.height - (_object.border_width * 2),
                    )

                # Convert image for tkinter
                self.tk_images[_object.master] = convert_image(_object, self.image)

        elif type(image) is str:
            # Open image
            self.image = pil.open(image)
            if _object is not None:
                # Resize image if size isn't specified
                if _object.width != 0 and _object.height != 0:
                    self.resize(
                        _object.width - (_object.border_width * 2),
                        _object.height - (_object.border_width * 2),
                    )

                # Convert image for tkinter
                self.tk_images[_object.master] = convert_image(_object, self.image)

        elif image is not None:
            self.image = image

            if _object is not None:
                self.tk_images[_object.master] = convert_image(_object, self.image)

    def resize(self, width, height):
        self.tk_images = {}
        if width != 0 and height != 0:
            self.image = self.image.resize(
                (
                    width,
                    height,
                ),
                pil.NEAREST,
            )
        return self

    def flip(self, direction="horizontal"):
        self.tk_images = {}
        if direction == "horizontal":
            self.image = self.image.transpose(pil.FLIP_LEFT_RIGHT)
        elif direction == "vertical":
            self.image = self.image.transpose(pil.FLIP_TOP_BOTTOM)
        return self

    def rotate(self, angle):
        self.tk_images = {}
        pil_img = self.image.rotate(angle, expand=True)
        self.image = pil_img
        return self

    def recolor(self, color):
        self.tk_images = {}
        pil_img = self.image.convert("RGBA")
        data = pil_img.getdata()

        color = colors_manager.Color(color)
        color = color.rgba
        new_data = [
            (
                *color[:3],
                standard_methods.clamp(data[i][3] - (255 - color[3]), 0, 255),
            )
            for i in range(len(data))
        ]
        return self._update_pil_data(pil_img, new_data)

    def set_transparency(self, transparency):
        self.tk_images = {}
        pil_img = self.image.convert("RGBA")
        data = pil_img.getdata()
        new_data = [
            (
                *data[i][:3],
                standard_methods.clamp(transparency, 0, 255),
            )
            for i in range(len(data))
        ]
        return self._update_pil_data(pil_img, new_data)

    def increment_transparency(self, transparency):
        self.tk_images = {}
        pil_img = self.image.convert("RGBA")
        data = pil_img.getdata()
        new_data = [
            (
                *data[i][:3],
                standard_methods.clamp(data[i][3] - transparency, 0, 255),
            )
            for i in range(len(data))
        ]
        return self._update_pil_data(pil_img, new_data)

    def set_relative_transparency(self, transparency, curve="lin", exponent=1):
        """
        Update transparency based on given curve.

        transparency: The new maximum transparency
        curve: The curve to use for updating transparency
        exponent: The exponent for the curve (only used if curve is "exp")
        """
        curves = {
            "exp": lambda x, n=exponent: math.pow(
                (math.pow(transparency, 1 / n) / 255 * x), n
            ),
            "lin": lambda x: transparency * (x / 255),
            "sqrt": lambda x: curves["exp"](x, 0.5),
            "quad": lambda x: curves["exp"](x, 2),
            "cubic": lambda x: curves["exp"](x, 3),
            "log": lambda x: transparency / math.log(255 + 1) * math.log(x + 1),
        }

        self.tk_images = {}
        pil_img = self.image.convert("RGBA")
        data = pil_img.getdata()
        new_data = [
            (
                *data[i][:3],
                standard_methods.clamp(int(curves[curve](data[i][3])), 0, 255),
            )
            for i in range(len(data))
        ]

        return self._update_pil_data(pil_img, new_data)

    def _update_pil_data(self, pil_img, new_data):
        pil_img.putdata(new_data)
        self.image = pil_img
        return self

    def tk_image(self, _object):
        if _object.master not in self.tk_images:
            self.tk_images[_object.master] = convert_image(_object, self.image)
        return self.tk_images[_object.master]


def convert_image(_object, image):
    # Handle Container objects
    if hasattr(_object, "_window"):
        # _object is a Container itself (when passed as master to create_image)
        tkinter_root = _object._window.root
    elif hasattr(_object.master, "_window"):
        # _object.master is a Container (when a widget is parented to a container)
        tkinter_root = _object.master._window.root
    else:
        # This is a regular window_internal object
        tkinter_root = _object.master.root

    return piltk.PhotoImage(image, master=tkinter_root)


def load_image(_object, image, return_both=False):
    """Load an image with PIL

    Args:
        _object (nebulatk.Widget): widget
        image (str): path to the image
        return_both (bool, optional): Request for both TkImage and PilImage. Defaults to False.

    Returns:
        TkImage: Tkinter-compatible image
    OR:
        TkImage: Tkinter-compatible image
        PilImage: Pil image
    """
    image_converted = None
    if image is not None:
        # Open image
        image = pil.open(image)

        # Resize image if size isn't specified
        if _object.width != 0 and _object.height != 0:
            image = image.resize(
                (
                    _object.width - (_object.border_width * 2),
                    _object.height - (_object.border_width * 2),
                ),
                pil.NEAREST,
            )

        # Convert image for tkinter
        image_converted = convert_image(_object, image)

    # Return both PhotoImage and PilImage objects if requested
    return (image_converted, image) if return_both else image_converted


def load_image_generic(window, image, return_both=False):
    """Alternative to load_image without resizing. Does not require a parent widget.

    Args:
        image (str): path to the image
        return_both (bool, optional): Request for both TkImage and PilImage. Defaults to False.

    Returns:
        TkImage: Tkinter-compatible image
    OR:
        TkImage: Tkinter-compatible image
        PilImage: Pil image
    """
    image_converted = None
    if image is not None:
        # Open image
        image = pil.open(image)

        # Convert image for tkinter
        image_converted = convert_image(window, image)

    # Return both PhotoImage and PilImage objects if requested
    return (image_converted, image) if return_both else image_converted


def create_image(fill, width, height, border, border_width, master):
    """Generate a new TkImage image

    Args:
        fill (color): fill color
        width (int): width
        height (int): height
        border (color): border color
        border_width (int): border_width

    Returns:
        TkImage: Tkinter-compatible image
    """
    # Create base image
    image = pil.new("RGBA", (width, height), (0, 0, 0, 255))
    # Generate corners of rectangle (0-indexed)
    shape = [(0, 0), (width - 1, height - 1)]

    # Draw rectangle on image
    image1 = pildraw.Draw(image)
    image1.rectangle(shape, fill=fill, outline=border, width=border_width)

    # Convert image
    image = Image(image, master)
    return image
