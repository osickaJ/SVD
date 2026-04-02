import pyvista as pv #type:ignore

FILTERS = ["linear", "butterfly", "loop"]
STEPS   = [0, 1, 3]
COLORS  = ["#4FC3F7", "#81C784", "#CE93D8"]

mesh = pv.Cube().triangulate()

plotter = pv.Plotter(shape=(3, 3), window_size=(1300, 1000))

for row, subfilter in enumerate(FILTERS):
    for col, step in enumerate(STEPS):
        subdivided = mesh if step == 0 else mesh.subdivide(step, subfilter=subfilter)
        label = f"{subfilter.capitalize()} — {'Original' if step == 0 else f'Step {step}'}"

        plotter.subplot(row, col)
        #plotter.add_text(f"{label}\n{subdivided.n_points} verts  {subdivided.n_cells} cells", font_size=10)
        plotter.add_mesh(subdivided, color=COLORS[col], show_edges=True, edge_color="white", smooth_shading=True)
        plotter.view_isometric()

plotter.link_views()
plotter.show()