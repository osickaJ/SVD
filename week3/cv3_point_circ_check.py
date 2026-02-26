import numpy as np
import matplotlib.pyplot as plt

def point_in_circle(A, B, C, P):
    mat = np.array([
        [A[0], A[1], A[0]**2 + A[1]**2, 1],
        [B[0], B[1], B[0]**2 + B[1]**2, 1],
        [C[0], C[1], C[0]**2 + C[1]**2, 1],
        [P[0], P[1], P[0]**2 + P[1]**2, 1]
    ])
    det = np.linalg.det(mat)

    if np.isclose(det, 0):
        return "The point is on the circle"
    elif det > 0:
        return "The point is inside the circle"
    else:
        return "The point is outside the circle"

def circumcircle(A, B, C):
    """
    Compute center and radius of circumcircle of triangle ABC
    """
    Ax, Ay = A
    Bx, By = B
    Cx, Cy = C

    D = 2 * (Ax*(By-Cy) + Bx*(Cy-Ay) + Cx*(Ay-By))

    Ux = ((Ax**2 + Ay**2)*(By-Cy) + (Bx**2 + By**2)*(Cy-Ay) + (Cx**2 + Cy**2)*(Ay-By)) / D
    Uy = ((Ax**2 + Ay**2)*(Cx-Bx) + (Bx**2 + By**2)*(Ax-Cx) + (Cx**2 + Cy**2)*(Bx-Ax)) / D

    center = np.array([Ux, Uy])
    radius = np.linalg.norm(center - np.array(A))

    return center, radius

if __name__ == "__main__":
    # Fixed points
    A = (0, 0)
    B = (1, 0)
    C = (0, 1)

    # Input P
    x, y = map(float, input("Enter coordinates of P (x y): ").split())
    P = (x, y)

    # Determine position
    result = point_in_circle(A, B, C, P)
    print(f"{result} ")

    # Compute circumcircle
    center, radius = circumcircle(A, B, C)

    # Plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal')

    # Plot triangle points
    ax.scatter(*A, label="A")
    ax.scatter(*B, label="B")
    ax.scatter(*C, label="C")

    # Plot P
    ax.scatter(*P, marker='x', s=100, label="P")

    # Plot circumcircle
    circle = plt.Circle(center, radius, fill=False)
    ax.add_patch(circle)

    # Plot center
    ax.scatter(center[0], center[1], marker='o', label="Center")

    # Formatting
    #ax.legend()
    ax.set_title("Circumcircle and Point Test")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid()

    plt.show()