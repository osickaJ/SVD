import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt

def trian_2D(points):
    pts_arr = np.asarray(points)
    if len(pts_arr) < 3:
        print("Error: Need at least 3 points for 2D triangulation.")
        return None
    tri = Delaunay(pts_arr)
    
    # Plotting
    plt.triplot(pts_arr[:, 0], pts_arr[:, 1], tri.simplices)
    plt.plot(pts_arr[:, 0], pts_arr[:, 1], 'o')
    plt.title("Delaunay Triangulation")
    plt.show()
    return tri

