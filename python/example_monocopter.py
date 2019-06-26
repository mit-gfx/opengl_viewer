import trimesh
from pygl_window import PyglWindow

fps = 30
window = PyglWindow(fps)

# Monocopter.
monocopter_mesh = trimesh.load("../resources/meshes/monocopter.ply")
monocopter = window.render_shape(monocopter_mesh.vertices, monocopter_mesh.faces,
                                 color=[0.809, 0.585, 0.480])

max_frame = 1024
for f in range(max_frame):
  t = f / fps
  monocopter.set_trs_transform(t, translation=[0, 0, -t / 100])

window.show()