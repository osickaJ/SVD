import numpy as np
import pyvista as pv

class CatmullClark:
    def __init__(self, mesh: pv.PolyData):
        self.mesh = mesh
        self.V = mesh.points
        self.nV = len(self.V)
        self.F = self._extract_faces(mesh)
        self.nF = len(self.F)

    def _extract_faces(self, mesh):
        faces = []
        arr = mesh.faces
        i = 0
        while i < len(arr):
            k = arr[i]
            faces.append(list(arr[i+1:i+1+k]))
            i += k + 1
        return faces

    def compute_face_points(self):
        return np.array([self.V[f].mean(axis=0) for f in self.F])

    def build_edge_map(self):
        edge_faces = {}
        for fi, face in enumerate(self.F):
            k = len(face)
            for i in range(k):
                a, b = face[i], face[(i+1)%k]
                key = (min(a,b), max(a,b))
                edge_faces.setdefault(key, []).append(fi)
        return edge_faces

    def compute_edge_points(self, face_points, edge_faces):
        edges = list(edge_faces.keys())
        edge_index = {e: self.nV + self.nF + i for i, e in enumerate(edges)}
        edge_points = []
        for (a,b), adj_faces in edge_faces.items():
            pts = [self.V[a], self.V[b]] + [face_points[fi] for fi in adj_faces]
            edge_points.append(np.mean(pts, axis=0))
        return np.array(edge_points), edge_index

    def compute_vertex_points(self, face_points, edge_faces):
        vertex_faces = [[] for _ in range(self.nV)]
        vertex_edges = [[] for _ in range(self.nV)]

        for fi, face in enumerate(self.F):
            for v in face:
                vertex_faces[v].append(fi)
        for a,b in edge_faces.keys():
            vertex_edges[a].append((a,b))
            vertex_edges[b].append((a,b))

        new_vertices = []
        for i in range(self.nV):
            n = len(vertex_faces[i])
            F = np.mean(face_points[vertex_faces[i]], axis=0)
            R = np.mean([(self.V[a]+self.V[b])/2 for a,b in vertex_edges[i]], axis=0)
            new_vertices.append((F + 2*R + (n-3)*self.V[i])/n)
        return np.array(new_vertices)

    def build_new_faces(self, edge_index):
        new_faces = []
        for fi, face in enumerate(self.F):
            fp_idx = self.nV + fi
            k = len(face)
            for i in range(k):
                v = face[i]
                v_next = face[(i+1)%k]
                v_prev = face[(i-1)%k]
                e_next = (min(v,v_next), max(v,v_next))
                e_prev = (min(v_prev,v), max(v_prev,v))
                new_faces.append([v, edge_index[e_next], fp_idx, edge_index[e_prev]])
        return new_faces

    def to_polydata(self, vertices, faces):
        cells = []
        for f in faces:
            cells.append(len(f))
            cells.extend(f)
        return pv.PolyData(vertices, np.array(cells))

    def subdivide(self):
        face_points = self.compute_face_points()
        edge_faces = self.build_edge_map()
        edge_points, edge_index = self.compute_edge_points(face_points, edge_faces)
        vertex_points = self.compute_vertex_points(face_points, edge_faces)
        new_vertices = np.vstack([vertex_points, face_points, edge_points])
        new_faces = self.build_new_faces(edge_index)
        return self.to_polydata(new_vertices, new_faces)

    def subdivide_n(self, steps):
        mesh = self.mesh
        for _ in range(steps):
            mesh = CatmullClark(mesh).subdivide()
        return mesh