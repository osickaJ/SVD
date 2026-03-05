import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d import Axes3D

# 1. Generate random 3D points
np.random.seed(42)
num_points = 20
points = np.random.rand(num_points, 3)  # (x, y, z) triplets
# 3. Create Delaunay triangulation (Tetrahedralization)
tri = Delaunay(points)

# 4. Setup 3D Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 5. Plot points
ax.scatter(points[:, 0], points[:, 1], points[:, 2], 
           color='red', label='Points')

# 6. Plot tetrahedra edges
# Each simplex has 4 points. We plot lines between them.
for simplex in tri.simplices:
    # Get the coordinates for the 4 vertices of the tetrahedron
    pts = points[simplex]
    # Plot edges between all pairs in the simplex
    for i in range(4):
        for j in range(i + 1, 4):
            ax.plot(pts[[i, j], 0], pts[[i, j], 1], pts[[i, j], 2], 'b-', alpha=0.5)

ax.set_title('3D Delaunay Tetrahedralization')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()