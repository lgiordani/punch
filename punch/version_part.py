# -*- coding: utf-8 -*-

class IntegerVersionPart:
    def __init__(self, value):
        if value is None:
            self.value = 0
        else:
            self.value = int(value)

    def inc(self):
        self.value = self.value + 1

    def reset(self):
        self.value = 0


class ValueListVersionPart:
    def __init__(self, value, allowed_values):
        if value is None:
            self.value = allowed_values[0]
        else:
            if value not in allowed_values:
                raise ValueError("The given value {} is not allowed, the list of possible values is {}", value,
                                 allowed_values)
            self.value = value

        self.values = allowed_values

    def inc(self):
        idx = self.values.index(self.value)
        self.value = self.values[(idx + 1) % len(self.values)]

    def reset(self):
        self.value = self.values[0]
