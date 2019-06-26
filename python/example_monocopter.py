import trimesh
import numpy as np
from pygl_window import PyglWindow

# Initialization.
fps = 30
window = PyglWindow(name='monocopter', fps=fps, xyz='ned', record=True)

# Load meshes.
monocopter_mesh = trimesh.load("../resources/meshes/monocopter.ply")
prop_mesh = trimesh.load("../resources/meshes/propeller.ply")

# Define your animation.
monocopter = window.render_shape(monocopter_mesh.vertices, monocopter_mesh.faces,
                                 color=[0.809, 0.585, 0.480])
prop = window.render_shape(prop_mesh.vertices, prop_mesh.faces,
                           color=[0.001, 0.564, 0.193])
prop_local_translate=np.array([-0.24, 0.15, 0])

max_frame = 256
for f in range(max_frame):
  t = f / fps
  copter_translate = np.array([0, 0, -t / 25], dtype=np.float32)
  theta = f / fps * 2.5
  c, s = np.cos(theta), np.sin(theta)
  copter_rotate = np.array([[c, s, 0],
                            [-s, c, 0],
                            [0, 0, 1]], dtype=np.float32)
  monocopter.set_trs_transform(t, translation=copter_translate, rotation=copter_rotate)

  # Propeller.
  prop_theta = f / fps * 10
  c, s = np.cos(prop_theta), np.sin(prop_theta)
  prop_rotate = np.array([[c, 0, -s],
                          [0, 1, 0],
                          [s, 0, c]], dtype=np.float32)
  prop.set_trs_transform(t, translation=copter_rotate @ prop_local_translate + copter_translate,
                         rotation=copter_rotate @ prop_rotate)

# Display.
window.show()
# You can also replace "monocopter.gif" with "monocopter.mp4".
window.export_video("monocopter.gif")