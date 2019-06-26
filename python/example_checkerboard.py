from pygl_viewer import *
import trimesh

option = PyglOption()
option["camera field of view"] = 60.0
option["camera aspect ratio"] = 4.0 / 3.0
option["height"] = 768
option["width"] = 1024
option["shadow acne bias"] = 0.005
option["shadow sampling angle"] = 0.57
option["shadow sampling number"] = 2
option["shadow"] = True

viewer = PyglViewer(option)

fps = 25
viewer.register_linear_timer(fps)

checker_size = 512
square_size = 32
checker_image = np.zeros((checker_size, checker_size, 3))
for i in range(checker_size):
  for j in range(checker_size):
    if (i // square_size - j // square_size) % 2:
      checker_image[i, j] = [157, 150, 143]
    else:
      checker_image[i, j] = [216, 208, 197]
checker_image /= 255

vertex = [[-1, 0, -1],
          [1, 0, -1],
          [-1, 0, 1],
          [1, 0, 1]]
face = [[0, 2, 3],
        [0, 3, 1]]
uv = [[0, 0, 1, 1],
      [0, 1, 0, 1]]
object_option = PyglOption()
object_option["model matrix"] = [[4, 0, 0, 0],
                                 [0, 1, 0, 0],
                                 [0, 0, 4, 0],
                                 [0, 0, 0, 1]]
object_option["ambient"] = [0.7, 0.7, 0.7]
object_option["diffuse"] = [1, 1, 1]
object_option["specular"] = [1, 1, 1]
object_option["shininess"] = 1.5
object_option["texture"] = np.reshape(checker_image, (checker_size * checker_size, 3)).T
object_option["uv"] = uv
object_option["texture row num"] = checker_size
object_option["texture col num"] = checker_size
object_option["texture mag filter"] = 'nearest'
viewer.add_static_object(vertex, face, object_option)

light_pos = [0, 1.9, 0.5]
light_option = PyglOption()
light_option["ambient"] = [0.17, 0.15, 0.14]
light_option["diffuse"] = [0.37, 0.35, 0.34]
light_option["specular"] = [0.37, 0.35, 0.34]
viewer.add_static_point_light(light_pos, light_option)

light_pos = [-0.5, 2.1, -0.5]
viewer.add_static_point_light(light_pos, light_option)

# Now let's make a moving cube.
cube = trimesh.load("../resources/meshes/cube.obj")
cube_option = PyglOption()
cube_option["model matrix"] = [[0.6, 0, 0, 0],
                               [0, 0.6, 0, 0],
                               [0, 0, 0.6, 0],
                               [0, 0, 0, 1]]
cube_option["ambient"] = [0.12, 0.33, 0.17]
cube_option["diffuse"] = [0.44, 0.56, 0.54]
cube_option["specular"] = [0.17, 0.84, 0.82]
cube_option["shininess"] = 4.0
max_frames = 1024
animator = PyglSamplingAnimator(max_frames)
for i in range(max_frames):
  mat = [[1, 0, 0, np.sin((i / fps / 4.0) * np.pi * 2.0)],
         [0, 1, 0, 0],
         [0, 0, 1, 0],
         [0, 0, 0, 1]]
  animator.add_sample(i / fps, mat)
viewer.add_dynamic_object(cube.vertices, cube.faces, animator, cube_option)

viewer.run()
viewer.cleanup()