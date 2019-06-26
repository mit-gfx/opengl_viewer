import numpy as np
from pygl_viewer import *

class PyglShape(object):
  def __init__(self, vertex, face, transform, color):
    self.vertex = np.array(vertex, dtype=np.float32)
    self.face = np.array(face, dtype=np.int)
    self.option = PyglOption()
    self.option["model matrix"] = transform
    if color == 'r':
      color3 = [1, 0, 0]
    elif color == 'g':
      color3 = [0, 1, 0]
    elif color == 'b':
      color3 = [0, 0, 1]
    elif color == 'k':
      color3 = [0, 0, 0]
    elif color == 'w':
      color3 = [1, 1, 1]
    elif color == 'y':
      color3 = [1, 1, 0]
    else:
      color3 = np.array(color, dtype=np.float32)

    self.option["ambient"] = color3
    self.option["diffuse"] = color3
    self.option["specular"] = color3

    self.option["smooth normal"] = False

    self.animator = None

  def set_trs_transform(self, time, translation=[0, 0, 0],
                        rotation=np.eye(3),
                        scaling=1):
    if self.animator is None:
      self.animator = PyglSamplingAnimator(-1)
    mat = np.eye(4)
    translation = np.array(translation, dtype=np.float32)
    rotation = np.array(rotation, dtype=np.float32)
    scaling = np.array(scaling)
    if scaling.size == 1:
      scaling = np.array([scaling, scaling, scaling])
    mat[:3, :3] = rotation @ np.diag(scaling)
    mat[:3, -1] = translation
    self.animator.add_sample(time, mat)

class PyglWindow(object):
  def __init__(self, fps):
    self.shapes = []

    # Initialize the viewer.
    option = PyglOption()
    option["height"] = 1000
    option["width"] = 1600
    option["background color"] = [0.86, 0.88, 0.90, 1.0]
    option["camera aspect ratio"] = 1600 / 1000
    option["camera pos"] = [-1.6, -0.8, -1.6]
    option["camera look at"] = [0.8, -0.5, 0.0]
    option["camera up"] = [0.0, 0.0, -1.0]
    option["camera pan speed"] = 0.004
    option["camera field of view"] = 45
    option["shadow acne bias"] = 0.005
    option["shadow sampling angle"] = 0.2
    option["shadow sampling number"] = 2
    option["shadow"] = False

    self.viewer = PyglViewer(option)
    self.viewer.register_linear_timer(fps)

    # Add ground.
    checker_size = 2
    square_size = 1
    checker_image = np.zeros((checker_size, checker_size, 3))
    for i in range(checker_size):
      for j in range(checker_size):
        if (i // square_size - j // square_size) % 2:
          checker_image[i, j] = [157, 150, 143]
        else:
          checker_image[i, j] = [216, 208, 197]
    checker_image /= 255

    vertex = [[-1, -1, 0],
              [-1, 1, 0],
              [1, -1, 0],
              [1, 1, 0]]
    face = [[0, 1, 2],
            [2, 1, 3]]
    scale = 1000
    uv = np.array([[-1, -1, 1, 1],
                   [-1, 1, -1, 1]], dtype=np.float32) / 2 * scale
    ground_option = PyglOption()
    ground_option["model matrix"] = [[scale, 0, 0, 0],
                                     [0, scale, 0, 0],
                                     [0, 0, 1, 0],
                                     [0, 0, 0, 1]]
    ground_option["ambient"] = [0.75, 0.77, 0.72]
    ground_option["diffuse"] = [0.84, 0.8, 0.81]
    ground_option["texture"] = np.reshape(checker_image, (checker_size * checker_size, 3)).T
    ground_option["uv"] = uv
    ground_option["texture row num"] = checker_size
    ground_option["texture col num"] = checker_size
    ground_option["texture mag filter"] = 'nearest'
    self.viewer.add_static_object(vertex, face, ground_option)

    # Add light.
    light_option = PyglOption()
    light_option["ambient"] = [0.54, 0.56, 0.51]
    light_option["diffuse"] = [0.55, 0.59, 0.56]
    light_option["specular"] = [0.21, 0.26, 0.24]
    light_pos = [0.2, -0.3, -1.5]
    self.viewer.add_static_point_light(light_pos, light_option)

  def render_shape(self, vertex, face,
                   translation=[0, 0, 0],
                   rotation=np.eye(3),
                   scaling=1,
                   color='r'):
    mat = np.eye(4)
    translation = np.array(translation, dtype=np.float32)
    rotation = np.array(rotation, dtype=np.float32)
    scaling = np.array(scaling)
    if scaling.size == 1:
      scaling = np.array([scaling, scaling, scaling])
    mat[:3, :3] = rotation @ np.diag(scaling)
    mat[:3, -1] = translation
    shape = PyglShape(vertex, face, mat, color)
    self.shapes.append(shape)
    return self.shapes[-1]

  def show(self):
    for shape in self.shapes:
      if shape.animator is None:
        self.viewer.add_static_object(shape.vertex, shape.face, shape.option)
      else:
        self.viewer.add_dynamic_object(shape.vertex, shape.face, shape.animator, shape.option)
    self.viewer.run()
    self.viewer.cleanup()