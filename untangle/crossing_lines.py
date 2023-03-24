from dataclasses import dataclass
from typing import List, Tuple

# Rewrite this code using complex numbers


@dataclass(frozen=True, repr=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True, repr=True)
class Line:
    a: Point
    b: Point

    def is_crossing(self, other: "Line") -> bool:
        """
        This function returns True when the line segments a1-a2 and b1-b2 cross.
        """

        def ccw(A: Point, B: Point, C: Point) -> bool:
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)

        return ccw(self.a, self.b, other.b) != ccw(other.a, self.b, other.b) and ccw(
            self.a, other.a, self.b
        ) != ccw(self.a, other.a, other.b)


@dataclass(frozen=True, repr=True)
class Polygon:
    points: List[Point]

    def polygon_check(polygon: "Polygon") -> bool:
        """
        This function returns True when the polygon outline does not cross itself.
        """
        N = len(polygon.points)
        for i in range(N):
            line_a = Line(a=polygon.points[i], b=polygon.points[(i + 1) % N])
            for j in range(i + 2, N):
                line_b = Line(polygon.points[j], polygon.points[(j + 1) % N])
                if line_a.is_crossing(line_b):
                    return False
        return True


polygon = Polygon(
    points=[
        Point(10.0, 12.0),
        Point(2.0, 2.0),
        Point(4.0, 5.0),
        Point(6.0, 8.0),
    ]
)


polygon.polygon_check()
