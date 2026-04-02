import numpy as np
import matplotlib.pyplot as plt

class Bspline:
    def __init__(self, body, stupen, uzlVektor):
        self.body = np.array(body, dtype=float)
        self.stupen = stupen
        self.uzlVektor = np.array(uzlVektor, dtype=float)
        self.n = len(self.body) - 1

    def najdiIndexUzlu(self, t):
        p = self.stupen
        n = self.n
        U = self.uzlVektor

        if t == U[n + 1]:
            return n

        for i in range(p, n + 1):
            if U[i] <= t < U[i + 1]:
                return i

        return None

    def deBoor(self, t):
        p = self.stupen
        U = self.uzlVektor
        k = self.najdiIndexUzlu(t)

        # copy control points
        d = [self.body[j].copy() for j in range(k - p, k + 1)]

        for r in range(1, p + 1):
            for j in range(p, r - 1, -1):
                i = k - p + j
                alpha = (t - U[i]) / (U[i + p - r + 1] - U[i])

                d[j] = (1 - alpha) * d[j - 1] + alpha * d[j]

        return d[p]

    def spocitejKrivku(self, pocet_bodu=100):
        U = self.uzlVektor
        t_min = U[self.stupen]
        t_max = U[self.n + 1]

        t_values = np.linspace(t_min, t_max, pocet_bodu)
        krivka = []

        for t in t_values:
            bod = self.deBoor(t)
            krivka.append(bod)

        return np.array(krivka)

    def vykresliKrivku(self):
        krivka = self.spocitejKrivku()

        x = krivka[:, 0]
        y = krivka[:, 1]

        x_body = self.body[:, 0]
        y_body = self.body[:, 1]

        plt.plot(x, y, label="B-spline")
        plt.plot(x_body, y_body, 'ro--', label="Ridici body")

        plt.legend()
        plt.title("B-spline krivka")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()

        plt.show()