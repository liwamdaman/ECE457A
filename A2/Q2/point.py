from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))