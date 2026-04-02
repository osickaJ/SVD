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
        krivka = [self.deBoor(t) for t in t_values]
        return np.array(krivka)

    def vykresliInteraktivni(self):
        fig, ax = plt.subplots()
        ax.set_aspect('equal', 'box')

        krivka = self.spocitejKrivku()
        curve_line, = ax.plot(krivka[:, 0], krivka[:, 1], 'b-', label="B-spline")
        control_line, = ax.plot(self.body[:, 0], self.body[:, 1], 'ro--', label="Ridici body")
        selected_point = [None]

        def on_press(event):
            if event.inaxes != ax:
                return
            distances = np.hypot(self.body[:, 0] - event.xdata, self.body[:, 1] - event.ydata)
            idx = np.argmin(distances)
            # adjust threshold based on your axes size
            if distances[idx] < 0.5:  
                selected_point[0] = idx

        def on_release(event):
            selected_point[0] = None

        def on_motion(event):
            idx = selected_point[0]
            if idx is None or event.inaxes != ax:
                return
            self.body[idx, 0] = event.xdata
            self.body[idx, 1] = event.ydata
            krivka_new = self.spocitejKrivku()
            curve_line.set_data(krivka_new[:, 0], krivka_new[:, 1])
            control_line.set_data(self.body[:, 0], self.body[:, 1])
            fig.canvas.draw_idle()

        fig.canvas.mpl_connect('button_press_event', on_press)
        fig.canvas.mpl_connect('button_release_event', on_release)
        fig.canvas.mpl_connect('motion_notify_event', on_motion)

        ax.legend()
        ax.set_title("Interaktivní B-spline")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.grid()
        plt.show()


if __name__ == "__main__":
    body = [
        [0, 0],
        [3, 5],
        [-3, 5],
        [0, 0],
        [2, 8]
    ]
    stupen = 3
    uzlVektor = [0, 0, 0, 0, 0.5, 1, 1, 1, 1]

    bspline = Bspline(body, stupen, uzlVektor)
    bspline.vykresliInteraktivni()