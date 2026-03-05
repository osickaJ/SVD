import numpy as np


class Point():
    def __init__(self, x: float, y: float, z: float, t: float):
        for name, val in [("x", x), ("y", y), ("z", z), ("t", t)]:
            if not isinstance(val, (int, float)):
                raise TypeError(f"Coordinate {name} must be a number, not {type(val).__name__}")
        self.x = x
        self.y = y
        self.z = z
        self.t = t # Fourth temperature coordinate

    def printPoint(self):
        print(f"[{self.x}, {self.y}, {self.z}] Temperature: {self.t}")


class Line():
    def __init__(self, point1:Point, point2:Point):
            self.point1 = point1
            self.point2 = point2

    def getLineLength(self):
        dx = self.point2.x - self.point1.x
        dy = self.point2.y - self.point1.y
        dz = self.point2.z - self.point1.z
        return (dx**2 + dy**2 + dz**2)**0.5
    

class Cube():
    def __init__(self, points: list[Point]):
        if len(points) != 8:
            raise ValueError("A cube must be defined by exactly 8 points.")
        # Sort points to ensure consistent indexing (000, 100, 010, 110, etc.)
        self.points = sorted(points, key=lambda p: (p.z, p.y, p.x))
       
        self.x_min, self.x_max = self.points[0].x, self.points[-1].x
        self.y_min, self.y_max = self.points[0].y, self.points[-1].y
        self.z_min, self.z_max = self.points[0].z, self.points[-1].z

    def get_temperature_at(self, x: float, y: float, z: float) -> float:
        xd = (x - self.x_min) / (self.x_max - self.x_min)
        yd = (y - self.y_min) / (self.y_max - self.y_min)
        zd = (z - self.z_min) / (self.z_max - self.z_min)

        c000, c100 = self.points[0].t, self.points[1].t
        c010, c110 = self.points[2].t, self.points[3].t
        c001, c101 = self.points[4].t, self.points[5].t
        c011, c111 = self.points[6].t, self.points[7].t

        a1 = c000 * (1 - xd) + c100 * xd
        a2 = c001 * (1 - xd) + c101 * xd
        a3 = c010 * (1 - xd) + c110 * xd
        a4 = c011 * (1 - xd) + c111 * xd

        a5 = a1 * (1 - yd) + a2 * yd
        a6 = a3 * (1 - yd) + a4 * yd

        return a5 * (1 - zd) + a6 * zd



    

