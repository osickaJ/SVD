import numpy as np
import matplotlib.pyplot as plt

class Bezier:
    def __init__(self, body, stupen,vahy):
        self.vahy=np.array(vahy)
        self.body = np.array(body)
        self.stupen = stupen
        self.M = np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]
        ])

    def vypisStupen(self):
        print(f"stupen je {self.stupen}")

    def _bazPolynom(self, t):
        return np.array([t**3, t**2, t, 1])

    def spocitejKrivku(self, pocet_bodu=100):
        t_v = np.linspace(0, 1, pocet_bodu)
        body_krivky = []

        for t in t_v:
            T = self._bazPolynom(t)
            bod_h=T @ self.M @ self.body

            x=bod_h[0]/bod_h[2]
            y=bod_h[1] / bod_h[2]

            
           
            body_krivky.append([x,y])

        return np.array(body_krivky)

    def vykresliKrivku(self):
        krivka = self.spocitejKrivku()

        # control points
        x_body = self.body[:, 0] / self.body[:, 2]
        y_body = self.body[:, 1] / self.body[:, 2]

        # curve points
        x = krivka[:, 0]
        y = krivka[:, 1]

        plt.plot(x, y, label="Bezier")
        plt.plot(x_body, y_body, 'ro--', label="Ridici body")

        plt.legend()
        plt.title("Bezier")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid()

        plt.show()