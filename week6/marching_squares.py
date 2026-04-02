Point = tuple[float, float]
Segment = tuple[Point, Point]

# Maps the 4-bit corner index to which pairs of edges the contour crosses.
# Corners are indexed: bottom-left=bit0, bottom-right=bit1, top-right=bit2, top-left=bit3
# Edges are indexed:   bottom=0, right=1, top=2, left=3
EDGE_TABLE = {
    0:  [],
    1:  [(3, 0)],
    2:  [(0, 1)],
    3:  [(3, 1)],
    4:  [(1, 2)],
    5:  [(3, 2), (0, 1)],   # saddle point — two segments
    6:  [(0, 2)],
    7:  [(3, 2)],
    8:  [(2, 3)],
    9:  [(0, 2)],
    10: [(0, 3), (1, 2)],   # saddle point — two segments
    11: [(1, 2)],
    12: [(1, 3)],
    13: [(0, 1)],
    14: [(3, 0)],
    15: [],
}


def lerp_edge(p_a: Point, p_b: Point, val_a: float, val_b: float, thr: float) -> Point:
    """Linearly interpolate along an edge to find where the thr-value crosses it."""
    t = (thr - val_a) / (val_b - val_a) if abs(val_b - val_a) > 1e-12 else 0.0
    return (p_a[0] + t * (p_b[0] - p_a[0]),
            p_a[1] + t * (p_b[1] - p_a[1]))


class Grid:
    def __init__(self, values: list[list[float]]):
        self.values = values
        self.rows = len(values)
        self.cols = len(values[0])

    def at(self, col: int, row: int) -> float:
        return self.values[row][col]


class MarchingSquares:

    def __init__(self, grid: Grid, thr: float):
        self.grid = grid
        self.thr = thr

    def _cell_segments(self, col: int, row: int) -> list[Segment]:
        g = self.grid

        # Corner values 
        v = {
            0: g.at(col,     row),
            1: g.at(col + 1, row),
            2: g.at(col + 1, row + 1),
            3: g.at(col,     row + 1),
        }

        # Corner positions (x = col index, y = row index)
        p = {
            0: ((col),     (row)),
            1: ((col + 1), (row)),
            2: ((col + 1), (row + 1)),
            3: ((col),     (row + 1)),
        }

        case = sum(1 << i for i in range(4) if v[i] < self.thr)

        if case in (0, 15):     # all above or all below — no contour
            return []

        # edge_points = {
        #     0: lerp_edge(p[0], p[1], v[0], v[1], self.thr),  # bottom
        #     1: lerp_edge(p[1], p[2], v[1], v[2], self.thr),  # right
        #     2: lerp_edge(p[2], p[3], v[2], v[3], self.thr),  # top
        #     3: lerp_edge(p[3], p[0], v[3], v[0], self.thr),  # left
        # }

        edge_points = { #uses midpoints all the time, lerp finds the exact crossing
            0: ((p[0][0] + p[1][0]) / 2, (p[0][1] + p[1][1]) / 2),  # bottom
            1: ((p[1][0] + p[2][0]) / 2, (p[1][1] + p[2][1]) / 2),  # right
            2: ((p[2][0] + p[3][0]) / 2, (p[2][1] + p[3][1]) / 2),  # top
            3: ((p[3][0] + p[0][0]) / 2, (p[3][1] + p[0][1]) / 2),  # left
        }

        return [(edge_points[e1], edge_points[e2]) for e1, e2 in EDGE_TABLE[case]]

    def extract(self) -> list[Segment]:
        segments = []
        for row in range(self.grid.rows - 1):
            for col in range(self.grid.cols - 1):
                segments.extend(self._cell_segments(col, row))
        return segments