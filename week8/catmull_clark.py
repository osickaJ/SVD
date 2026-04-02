"""
One step of Catmull-Clark subdivision on a cube/prism using PyVista.

Catmull-Clark subdivision works in 3 steps per face:
  1. Face points   — centroid of each face
  2. Edge points   — average of the two face-points adjacent to an edge
                     and the two endpoints of that edge
  3. Vertex points — weighted average using adjacent face/edge points

The resulting mesh has one quad per (original face × original vertex-per-face),
so a cube (6 quad faces) produces 6 × 4 = 24 quads after one step.
"""

import numpy as np
import pyvista as pv #type:ignore
from collections import defaultdict


# ──────────────────────────────────────────────
# 1. Build the input mesh (cube)
# ──────────────────────────────────────────────

def make_cube():
    """Return vertices and quad faces of a unit cube centred at origin."""
    v = np.array([
        [-1, -1, -1],
        [ 1, -1, -1],
        [ 1,  1, -1],
        [-1,  1, -1],
        [-1, -1,  1],
        [ 1, -1,  1],
        [ 1,  1,  1],
        [-1,  1,  1],
    ], dtype=float)

    # Six quad faces (vertex indices, CCW when viewed from outside)
    faces = [
        [0, 3, 2, 1],  # bottom  (-Z)
        [4, 5, 6, 7],  # top     (+Z)
        [0, 1, 5, 4],  # front   (-Y)
        [2, 3, 7, 6],  # back    (+Y)
        [0, 4, 7, 3],  # left    (-X)
        [1, 2, 6, 5],  # right   (+X)
    ]
    return v, faces


# ──────────────────────────────────────────────
# 2. Catmull-Clark — one subdivision step
# ──────────────────────────────────────────────

def catmull_clark_one_step(vertices, faces):
    """
    Apply one step of Catmull-Clark subdivision.

    Parameters
    ----------
    vertices : (N, 3) array of float
    faces    : list of lists of int  (each list = vertex indices of one polygon)

    Returns
    -------
    new_vertices : (M, 3) array of float
    new_faces    : list of 4-element lists of int  (all quads)
    """
    vertices = np.asarray(vertices, dtype=float)
    n_orig = len(vertices)

    # ── Step 1: face points ──────────────────────────────────────────────────
    face_points = np.array([vertices[f].mean(axis=0) for f in faces])
    # stored at indices [n_orig .. n_orig + n_faces - 1]

    # ── Step 2: edge points ──────────────────────────────────────────────────
    # Collect edges and which faces they belong to
    edge_faces = defaultdict(list)          # frozenset{a,b} -> [face_idx, ...]
    for fi, face in enumerate(faces):
        n = len(face)
        for i in range(n):
            e = frozenset((face[i], face[(i + 1) % n]))
            edge_faces[e].append(fi)

    edges = list(edge_faces.keys())
    edge_index = {e: n_orig + len(faces) + ei for ei, e in enumerate(edges)}

    edge_point_coords = []
    for e in edges:
        a, b = tuple(e)
        adj_face_pts = face_points[edge_faces[e]]          # (1 or 2, 3)
        edge_pt = np.vstack([vertices[[a, b]], adj_face_pts]).mean(axis=0)
        edge_point_coords.append(edge_pt)
    edge_points = np.array(edge_point_coords)

    # ── Step 3: updated original vertex points ───────────────────────────────
    # For each original vertex v:
    #   F = average of face-points of faces touching v
    #   R = average of edge mid-points of edges touching v
    #   n = valence (number of touching faces)
    #   new_v = (F + 2R + (n-3)*v) / n

    vertex_faces = defaultdict(list)
    vertex_edges = defaultdict(list)
    for fi, face in enumerate(faces):
        n = len(face)
        for i, vi in enumerate(face):
            vertex_faces[vi].append(fi)
            e = frozenset((face[i], face[(i + 1) % n]))
            vertex_edges[vi].append(e)
            e2 = frozenset((face[(i - 1) % n], face[i]))
            vertex_edges[vi].append(e2)

    new_orig_points = []
    for vi in range(n_orig):
        adj_fi = list(set(vertex_faces[vi]))
        adj_edges = list(set(vertex_edges[vi]))
        n_val = len(adj_fi)

        F = face_points[adj_fi].mean(axis=0)
        R = np.array([(vertices[list(e)].mean(axis=0)) for e in adj_edges]).mean(axis=0)
        new_v = (F + 2 * R + (n_val - 3) * vertices[vi]) / n_val
        new_orig_points.append(new_v)
    new_orig_points = np.array(new_orig_points)

    # ── Assemble all new vertices ────────────────────────────────────────────
    # Layout: [updated originals | face points | edge points]
    all_vertices = np.vstack([new_orig_points, face_points, edge_points])

    # ── Build new quad faces ─────────────────────────────────────────────────
    # Each original face (with k vertices) spawns k quads:
    #   [orig_v_i, edge_point(v_i, v_{i+1}), face_point, edge_point(v_{i-1}, v_i)]
    new_faces = []
    for fi, face in enumerate(faces):
        k = len(face)
        fp_idx = n_orig + fi
        for i in range(k):
            vi      = face[i]
            vi_next = face[(i + 1) % k]
            vi_prev = face[(i - 1) % k]

            ep_next = edge_index[frozenset((vi, vi_next))]
            ep_prev = edge_index[frozenset((vi_prev, vi))]

            new_faces.append([vi, ep_next, fp_idx, ep_prev])

    return all_vertices, new_faces


# ──────────────────────────────────────────────
# 3. Convert to PyVista PolyData
# ──────────────────────────────────────────────

def to_polydata(vertices, faces):
    """Convert vertex/face lists to a PyVista PolyData mesh."""
    cells = []
    for f in faces:
        cells.append(len(f))
        cells.extend(f)
    cells = np.array(cells, dtype=np.int_)
    return pv.PolyData(np.array(vertices, dtype=float), cells)


# ──────────────────────────────────────────────
# 4. Main – visualise side-by-side
# ──────────────────────────────────────────────

def catmull_clark_n_steps(vertices, faces, steps):
    """Apply Catmull-Clark subdivision for a given number of steps."""
    for _ in range(steps):
        vertices, faces = catmull_clark_one_step(vertices, faces)
    return vertices, faces


def main():
    # ── Colours for each subplot (original + 3 steps) ────────────────────────
    COLORS = ["#4FC3F7", "#81C784", "#FFB74D", "#CE93D8"]

    # ── Build all four meshes up front ───────────────────────────────────────
    verts, faces = make_cube()
    stages = [(verts, faces)]                         # step 0 = original
    for _ in range(3):
        v, f = catmull_clark_one_step(*stages[-1])
        stages.append((v, f))

    labels    = ["Original Cube", "Step 1", "Step 2", "Step 3"]
    positions = [(0, 0), (0, 1), (1, 0), (1, 1)]     # row, col in 2x2 grid

    print("Mesh progression:")
    for label, (v, f) in zip(labels, stages):
        print(f"  {label:<14}: {len(v):5d} vertices  {len(f):5d} faces")

    # ── 2x2 plotter ──────────────────────────────────────────────────────────
    plotter = pv.Plotter(shape=(2, 2), window_size=(1200, 900))

    for (row, col), (v, f), label, color in zip(positions, stages, labels, COLORS):
        mesh = to_polydata(v, f)
        plotter.subplot(row, col)
        plotter.add_text(
            f"{label}\n{len(v)} verts  {len(f)} faces",
            font_size=11,
        )
        plotter.add_mesh(mesh,
                         color=color,
                         show_edges=True,
                         edge_color="white",
                         opacity=0.95,
                         smooth_shading=True)
        plotter.view_isometric()

    plotter.link_views()   # rotate all four together
    plotter.show()


if __name__ == "__main__":
    main()