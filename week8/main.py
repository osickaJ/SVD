import numpy as np
import pyvista as pv
from catmulclass import CatmullClark

def make_cube_mesh():
    vertices = np.array([
        [-1, -1, -1],
        [ 1, -1, -1],
        [ 1,  1, -1],
        [-1,  1, -1],
        [-1, -1,  1],
        [ 1, -1,  1],
        [ 1,  1,  1],
        [-1,  1,  1],
    ], dtype=float)

    faces = [
        [0, 3, 2, 1],
        [4, 5, 6, 7],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 4, 7, 3],
        [1, 2, 6, 5],
    ]

    # Convert to PyVista format
    cells = []
    for f in faces:
        cells.append(len(f))
        cells.extend(f)

    return pv.PolyData(vertices, np.array(cells))

def subdivide_n(mesh, steps):
    for _ in range(steps):
        mesh = CatmullClark(mesh).subdivide()
    return mesh

def main():
    mesh0 = make_cube_mesh()

    # Generate subdivision stages
    stages = [mesh0]
    for _ in range(3):
        stages.append(subdivide_n(stages[-1], 1))

    plotter = pv.Plotter(shape=(2, 2), window_size=(1200, 900))

    for i, mesh in enumerate(stages):
        r, c = divmod(i, 2)
        plotter.subplot(r, c)

        plotter.add_mesh(
            mesh,
            show_edges=True,
            edge_color="white",
            opacity=0.9,
            smooth_shading=True
        )

        plotter.add_text(
            f"Step {i}\n{mesh.n_points} verts  {mesh.n_cells} faces",
            font_size=10
        )

        plotter.view_isometric()

    plotter.link_views()
    plotter.show()


if __name__ == "__main__":
    main()