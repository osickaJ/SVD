import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay

# 1. Generate random points
np.random.seed(42)
num_points = 20
points = np.random.rand(num_points, 2)  # (x, y) pairs

# 2. Sort points lexicographically by x-coordinate
points_sorted = points[np.argsort(points[:, 0])]

# 3. Create Delaunay triangulation
tri = Delaunay(points_sorted)

# 4. Plot points
plt.figure(figsize=(8,6))
plt.scatter(points_sorted[:,0], points_sorted[:,1], color='red', label='Points')

# 5. Plot triangles
for simplex in tri.simplices:
    plt.plot(points_sorted[simplex, 0], points_sorted[simplex, 1], 'b-')

plt.title('Random Scatter and Lexicographical Triangulation (by x)')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()