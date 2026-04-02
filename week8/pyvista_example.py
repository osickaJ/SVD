import numpy as np
import pyvista as pv # type:ignore

np.random.seed(42)

points = np.random.randn(20,3)
points_polydata = pv.PolyData(points)
print(points_polydata)

#points_polydata.plot(point_size = 10, render_points_as_spheres = True, color = 'red')

faces = np.hstack([[3,0,1,2],[4,4,5,10,11]])
mesh = pv.PolyData(points,faces)
print(mesh)

print(mesh.get_cell(0))

plane = pv.examples.load_airplane()
#plane.plot()

plotter1 = pv.Plotter(shape=(1,2))

sphere = pv.Sphere()
cone = pv.Arrow()

plotter1.subplot(0,0)
plotter1.add_mesh(sphere, color = 'blue')
plotter1.subplot(0,1)
plotter1.add_mesh(cone, color = 'red')
#plotter1.show()
def main():
    mesh = pv.Cube().triangulate()  # ← key step

    plotter = pv.Plotter(shape=(1, 2))

    for i in range(2):
        plotter.subplot(i // 2, i % 2)

        if i == 0:
            m = mesh
        else:
            m = mesh.subdivide(i, subfilter='loop')  # now valid

        plotter.add_text(f"Step {i}", font_size=10)
        plotter.add_mesh(m, show_edges=True)
        plotter.view_isometric()

    plotter.link_views()
    plotter.show()

if __name__ == "__main__":
    main()