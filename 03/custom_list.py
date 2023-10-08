"""
Реализовать класс CustomList наследованием от list
"""


class CustomList(list):
    """Кастом класс"""

    def __init__(self, *args):
        super().__init__(*args)
        self._check_numeric_values()

    def _check_numeric_values(self):
        for item in self:
            if not isinstance(item, (int, float)):
                raise TypeError(
                    "All elements of the list must be numeric values"
                )

    def __add__(self, other):
        if isinstance(other, list):
            other = CustomList(other)
        elif not isinstance(other, CustomList):
            raise TypeError
        result = CustomList(self)
        result.extend([0] * (len(other) - len(result)))
        for i, item in enumerate(other):
            result[i] += item
        return result

    def __radd__(self, other):
        if isinstance(other, list):
            other = CustomList(other)
        elif not isinstance(other, CustomList):
            raise TypeError
        result = CustomList(self)
        result.extend([0] * (len(other) - len(result)))
        for i, item in enumerate(other):
            result[i] += item
        return result

    def __sub__(self, other):
        if isinstance(other, list):
            other = CustomList(other)
        elif not isinstance(other, CustomList):
            raise TypeError
        result = CustomList(self)
        result.extend([0] * (len(other) - len(result)))
        for i, item in enumerate(other):
            result[i] -= item
        return result

    def __rsub__(self, other):
        if isinstance(other, list):
            other = CustomList(other)

        if not isinstance(other, CustomList):
            raise TypeError

        result = CustomList()
        max_len = max(len(self), len(other))

        for i in range(max_len):
            self_val = self[i] if i < len(self) else 0
            other_val = other[i] if i < len(other) else 0
            result.append(other_val - self_val)
        return result

    def __eq__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) == sum(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) > sum(other)
        raise TypeError

    def __ge__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) >= sum(other)
        raise TypeError

    def __lt__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) < sum(other)
        raise TypeError

    def __le__(self, other):
        if isinstance(other, (list, CustomList)):
            return sum(self) <= sum(other)
        raise TypeError

    def __str__(self):
        return f"{super().__str__()} (Sum: {sum(self)})"
