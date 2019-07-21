import numpy as np
import sys
import os
import imageio
import skvideo.io
from datetime import datetime
from pygl_viewer import *

def export_gif(gif_name, folder, format='{:d}.png'):
  images = []
  frame_idx = 0
  while True:
    frame_name = os.path.join(folder, format.format(frame_idx))
    if not os.path.exists(frame_name):
      imageio.mimsave(gif_name, images)
      break
    else:
      images.append(imageio.imread(frame_name))
      frame_idx += 1

def export_mp4(mp4_name, folder, format='{:d}.png'):
  images = []
  frame_idx = 0
  while True:
    frame_name = os.path.join(folder, format.format(frame_idx))
    if not os.path.exists(frame_name):
      images = np.array(images)
      skvideo.io.vwrite(mp4_name, images)
      break
    else:
      images.append(imageio.imread(frame_name))
      frame_idx += 1

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
    elif color == 'm':
      color3 = [1, 0, 1]
    elif color == 'c':
      color3 = [0, 1, 1]
    else:
      color3 = np.array(color, dtype=np.float32)

    self.option["ambient"] = color3
    self.option["diffuse"] = color3
    self.option["specular"] = color3

    self.option["smooth normal"] = False

    self.animator = None

  def set_trs_transform(self, time, translation=(0, 0, 0),
                        rotation=np.eye(3),
                        scaling=1):
    if self.animator is None:
      self.animator = PyglSamplingAnimator(-1)
    mat = np.eye(4)
    rotation = np.asarray(rotation, dtype=np.float32)
    scaling = np.asarray(scaling)
    if scaling.size == 1:
      scaling = np.array([scaling, scaling, scaling])
    mat[:3, :3] = rotation @ np.diag(scaling)
    mat[:3, -1] = translation
    self.animator.add_sample(time, mat)

class PyglWindow(object):
  def __init__(self, name, fps, xyz='xyz', height=800, width=1280, record=False):
    self.shapes = []

    # For recording data.
    self.name = name
    self.record_folder = None
    if record:
      # Create a folder.
      now = datetime.now()
      folder = name + '_%d_%d_%d_%d_%d_%d' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
      os.makedirs(folder, exist_ok=True)
      self.record_folder = folder

    # Initialize the viewer.
    option = PyglOption()
    option["height"] = height
    option["width"] = width
    option["background color"] = [0.86, 0.88, 0.90, 1.0]
    option["camera aspect ratio"] = 1600 / 1000
    if xyz == 'ned':
      option["camera pos"] = [-1, -0.25, -0.8]
      option["camera look at"] = [0.2, -0.1, 0.0]
      option["camera up"] = [0.0, 0.0, -1.0]
    elif xyz == 'xyz':
      option["camera pos"] = [-0.25, 0.8, 1]
      option["camera look at"] = [-0.1, 0, -0.2]
      option["camera up"] = [0, 1, 0]
    else:
      print('Unsupported xyz coordinates:', xyz)
      sys.exit(0)
    option["camera pan speed"] = 0.004
    option["camera field of view"] = 45
    option["record folder"] = '' if self.record_folder is None else self.record_folder
    option["shadow acne bias"] = 0.005
    option["shadow sampling angle"] = 0.2
    option["shadow sampling number"] = 2
    option["shadow"] = False
    option["window name"] = name

    self.viewer = PyglViewer(option)
    self.viewer.register_pybinding_default_components(fps)

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
                   translation=(0, 0, 0),
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

  def render_sphere(self, center=(0, 0, 0), radius=1,
                    translation=(0, 0, 0),
                    rotation=np.eye(3),
                    scaling=1,
                    color='r'):
    center = np.array(center, dtype=np.float32)
    # theta \in [0, 2pi], phi \in [-pi / 2, pi / 2].
    theta_num = 16
    phi_num = 8
    dtheta = 2.0 * np.pi / theta_num
    dphi = np.pi / phi_num
    vertices = np.zeros((theta_num * (phi_num - 1) + 2, 3))
    faces = np.zeros((theta_num * 2 + (phi_num - 2) * theta_num * 2, 3), dtype=np.int)
    vertices[0] = [0.0, 0.0, 1.0]
    for i in range(theta_num):
      vertices[1 + i] = [
        np.cos(np.pi / 2.0 - dphi) * np.cos(i * dtheta),
        np.cos(np.pi / 2.0 - dphi) * np.sin(i * dtheta),
        np.sin(np.pi / 2.0 - dphi)
      ]
      faces[i] = [0, i + 1, i + 2]
    faces[theta_num - 1, 2] = 1

    for i in range(phi_num - 2):
      phi = np.pi / 2.0 - dphi * (i + 2)
      for j in range(theta_num):
        vertices[1 + theta_num * (i + 1) + j] = [
          np.cos(phi) * np.cos(j * dtheta),
          np.cos(phi) * np.sin(j * dtheta),
          np.sin(phi)
        ]
        faces[theta_num * (2 * i + 1) + 2 * j] = [
          1 + theta_num * (i + 1) + j,
          1 + theta_num * (i + 1) + j + 1,
          1 + theta_num * i + j
        ]
        faces[theta_num * (2 * i + 1) + 2 * j + 1] = [
          1 + theta_num * (i + 1) + j + 1,
          1 + theta_num * i + j + 1,
          1 + theta_num * i + j
        ]
      faces[theta_num * (2 * i + 3) - 2, 1] = 1 + theta_num * (i + 1)
      faces[theta_num * (2 * i + 3) - 1, 0] = 1 + theta_num * (i + 1)
      faces[theta_num * (2 * i + 3) - 1, 1] = 1 + theta_num * i
    vertices[1 + theta_num * (phi_num - 1)] = [0.0, 0.0, -1.0]

    for i in range(theta_num):
      faces[theta_num * (2 * phi_num - 3) + i] = [
        1 + theta_num * (phi_num - 2) + i + 1,
        1 + theta_num * (phi_num - 2) + i,
        1 + theta_num * (phi_num - 1)
      ]
    faces[2 * theta_num * (phi_num - 1) - 1, 0] = 1 + theta_num * (phi_num - 2)
    vertices = vertices * radius + center
    return self.render_shape(vertices, faces, translation, rotation, scaling, color)

  def render_cylinder(self, center, dir, radius, height,
                      translation=(0, 0, 0),
                      rotation=np.eye(3),
                      scaling=1,
                      color='r'):
    center = np.array(center, dtype=np.float32)
    dir = np.array(dir, dtype=np.float32)

    # Create a local coordinate.
    xyz = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])]
    x = xyz[np.argmax([np.linalg.norm(np.cross(n, dir)) for n in xyz])]
    x = np.cross(x, dir)
    x /= np.linalg.norm(x)
    y = np.cross(dir, x)

    n = 6
    d = np.pi * 2.0 / n
    vertices = [center + dir * height / 2.0, center - dir * height / 2.0]
    faces = []
    for i in range(n):
      v = (np.cos(d * i) * x + np.sin(d * i) * y) * radius
      vertices.append(vertices[0] + v)
      vertices.append(vertices[1] + v)
      i00 = 2 + i * 2 + 1
      i01 = 2 + (i * 2 + 3) % (2 * n)
      i10 = 2 + i * 2
      i11 = 2 + (i * 2 + 2) % (2 * n)
      faces.append([i00, i01, i10])
      faces.append([i10, i01, i11])
      faces.append([i10, i11, 0])
      faces.append([i01, i00, 1])
    vertices = np.array(vertices, dtype=np.float64)
    faces = np.array(faces)
    return self.render_shape(vertices, faces, translation, rotation, scaling, color)

  def render_cube(self, center, size,
                  translation=(0, 0, 0),
                  rotation=np.eye(3),
                  scaling=1, color='r'):
    vertices = np.array([
      [-0.5, -0.5, -0.5],
      [-0.5, -0.5, 0.5],
      [-0.5, 0.5, -0.5],
      [-0.5, 0.5, 0.5],
      [0.5, -0.5, -0.5],
      [0.5, -0.5, 0.5],
      [0.5, 0.5, -0.5],
      [0.5, 0.5, 0.5]
    ]) * size + center
    faces = np.array([
      [0, 2, 6],
      [0, 6, 4],
      [1, 5, 7],
      [1, 7, 3],
      [7, 5, 4],
      [7, 4, 6],
      [3, 7, 6],
      [3, 6, 2],
      [1, 3, 2],
      [1, 2, 0],
      [1, 0, 4],
      [1, 4, 5]
    ])
    return self.render_shape(vertices, faces, translation, rotation, scaling, color)

  def render_arrow(self, tip, tail, radius=0.012, tip_length=0.15, tip_radius=0.024,
                   translation=(0, 0, 0),
                   rotation=np.eye(3),
                   scaling=1, color='r'):
    tip = np.array(tip, dtype=np.float32)
    tail = np.array(tail, dtype=np.float32)
    dir = tip - tail
    height = np.linalg.norm(dir)
    dir /= height
    # Draw the cylinder.
    cylinder_height = height - tip_length
    cylinder = self.render_cylinder(center=tail + dir * cylinder_height / 2.0, dir=dir, radius=radius,
                                    height=cylinder_height, translation=translation, rotation=rotation,
                                    scaling=scaling, color=color)
    del self.shapes[-1]
    # Draw the cone.
    cone = self.render_cone(center=tail + dir * cylinder_height, dir=dir, radius=tip_radius, height=tip_length,
                            translation=translation, rotation=rotation, scaling=scaling, color=color)
    del self.shapes[-1]
    # Assemble the arrow.
    v_cylinder, f_cylinder = cylinder.vertex, cylinder.face
    v_cone, f_cone = cone.vertex, cone.face
    v_arrow = np.vstack([v_cylinder, v_cone])
    f_arrow = np.vstack([f_cylinder, f_cone + v_cylinder.shape[0]])
    return self.render_shape(v_arrow, f_arrow, translation, rotation, scaling, color)

  def render_cone(self, center, dir, radius, height,
                  translation=(0, 0, 0),
                  rotation=np.eye(3),
                  scaling=1,
                  color='r'):
    center = np.array(center, dtype=np.float32)
    dir = np.array(dir, dtype=np.float32)

    # Create a local coordinate.
    xyz = [np.array([1.0, 0.0, 0.0]), np.array([0.0, 1.0, 0.0]), np.array([0.0, 0.0, 1.0])]
    x = xyz[np.argmax([np.linalg.norm(np.cross(n, dir)) for n in xyz])]
    x = np.cross(x, dir)
    x /= np.linalg.norm(x)
    y = np.cross(dir, x)

    n = 6
    d = np.pi * 2.0 / n
    vertices = [center, center + height * dir]
    faces = []
    for i in range(n):
      p = center + radius * (np.cos(d * i) * x + np.sin(d * i) * y)
      vertices.append(p)
      j = (i + 1) % n
      faces.append([0, j + 2, i + 2])
      faces.append([i + 2, j + 2, 1])
    vertices = np.array(vertices, dtype=np.float64)
    faces = np.array(faces)
    return self.render_shape(vertices, faces, translation, rotation, scaling, color)

  def show(self):
    for shape in self.shapes:
      if shape.animator is None:
        self.viewer.add_static_object(shape.vertex, shape.face, shape.option)
      else:
        self.viewer.add_dynamic_object(shape.vertex, shape.face, shape.animator, shape.option)
    self.viewer.run()
    self.viewer.cleanup()

  def export_video(self, name):
    if not self.record_folder:
      print('Cannot export videos. Please set record=True when creating PyglWindow.')
      sys.exit(0)
    if '.gif' in name:
      export_gif(name, self.record_folder)
    elif '.mov' in name:
      export_mp4(name, self.record_folder)
    else:
      print('Unsupported video name:', name)