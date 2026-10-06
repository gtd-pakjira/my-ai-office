from enum import Enum


class ThinkingHat(str, Enum):
    WHITE = "WHITE"
    RED = "RED"
    BLACK = "BLACK"
    YELLOW = "YELLOW"
    GREEN = "GREEN"
    BLUE = "BLUE"


HAT_ORDER = [
    ThinkingHat.WHITE,
    ThinkingHat.RED,
    ThinkingHat.BLACK,
    ThinkingHat.YELLOW,
    ThinkingHat.GREEN,
    ThinkingHat.BLUE,
]


class HatController:
    def __init__(self):
        self.current_index = 0

    @property
    def current_hat(self) -> ThinkingHat:
        return HAT_ORDER[self.current_index]

    def move_forward(self) -> ThinkingHat:
        if self.current_index >= len(HAT_ORDER) - 1:
            raise ValueError("Already at the last hat")

        self.current_index += 1
        return self.current_hat

    def move_backward(self) -> ThinkingHat:
        if self.current_index <= 0:
            raise ValueError("Already at the first hat")

        self.current_index -= 1
        return self.current_hat

    def can_move_forward(self) -> bool:
        return self.current_index < len(HAT_ORDER) - 1

    def can_move_backward(self) -> bool:
        return self.current_index > 0