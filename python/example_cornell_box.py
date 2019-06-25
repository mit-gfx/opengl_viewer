from pygl_viewer import *
import numpy as np

option = PyglOption()
option["camera field of view"] = 45.0
option["camera aspect ratio"] = 1.0
option["height"] = 800
option["width"] = 800
option["camera pos"] = [0, 0, 1]
option["camera look at"] = [0, 0, 0]
option["camera up"] = [0, 1, 0]
option["shadow acne bias"] = 0.01
option["shadow sampling angle"] = 0.5
option["shadow"] = False

viewer = PyglViewer(option)

# Ground.
object_options = PyglOption()
object_options["ambient"] = [0.5, 0, 0]
object_options["diffuse"] = [0.5, 0, 0]
object_options["model matrix"] = np.array([[1, 0, 0, 0],
                                           [0, 1, 0, -1],
                                           [0, 0, 1, 0],
                                           [0, 0, 0, 1]])
vertex = np.array([[-1, 0, -1],
                   [1, 0, -1],
                   [-1, 0, 1],
                   [1, 0, 1]])
face = np.array([[0, 2, 3],
                 [0, 3, 1]])
gray = np.array([0.85, 0.85, 0.85])
viewer.add_static_object(vertex, face, object_options)

object_options["model matrix"] = [[1, 0, 0, 0],
                                  [0, -1, 0, 1],
                                  [0, 0, -1, 0],
                                  [0, 0, 0, 1]]
object_options["ambient"] = [0, 0.5, 0]
object_options["diffuse"] = [0, 0.5, 0]
viewer.add_static_object(vertex, face, object_options)

object_options["model matrix"] = [[1, 0, 0, 0],
                                  [0, 0, -1, 0],
                                  [0, 1, 0, -1],
                                  [0, 0, 0, 1]]
object_options["ambient"] = [0, 0, 0.5]
object_options["diffuse"] = [0, 0, 0.5]
viewer.add_static_object(vertex, face, object_options)

object_options["model matrix"] = [[0, 1, 0, -1],
                                  [-1, 0, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]]
object_options["ambient"] = [0.5, 0.5, 0]
object_options["diffuse"] = [0.5, 0.5, 0]
viewer.add_static_object(vertex, face, object_options)

object_options["model matrix"] = [[0, -1, 0, 1],
                                  [1, 0, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]]
object_options["ambient"] = [0, 0.5, 0.5]
object_options["diffuse"] = [0, 0.5, 0.5]
viewer.add_static_object(vertex, face, object_options)


object_options["model matrix"] = [[0.25, 0, 0, 0],
                                  [0, 0.25, 0, -0.5],
                                  [0, 0, 0.25, 0],
                                  [0, 0, 0, 1]]
object_options["ambient"] = gray
viewer.add_static_object(vertex, face, object_options)
object_options["model matrix"] = [[0.25, 0, 0, 0],
                                  [0, -0.25, 0, 0.5],
                                  [0, 0, -0.25, 0],
                                  [0, 0, 0, 1]]
viewer.add_static_object(vertex, face, object_options)
object_options["model matrix"] = [[0.25, 0, 0, 0],
                                  [0, 0, -0.25, 0],
                                  [0, 0.25, 0, -0.5],
                                  [0, 0, 0, 1]]
viewer.add_static_object(vertex, face, object_options)
object_options["model matrix"] = [[0, 0.25, 0, -0.5],
                                  [-0.25, 0, 0, 0],
                                  [0, 0, 0.25, 0],
                                  [0, 0, 0, 1]]
viewer.add_static_object(vertex, face, object_options)
object_options["model matrix"] = [[0, -0.25, 0, 0.5],
                                  [0.25, 0, 0, 0],
                                  [0, 0, 0.25, 0],
                                  [0, 0, 0, 1]]
viewer.add_static_object(vertex, face, object_options)

light_option = PyglOption()
light_option["ambient"] = gray * 0.5
light_option["diffuse"] = gray * 0.5
light_option["specular"] = gray * 0.5
viewer.add_static_point_light([0.25, 0, 0], light_option)
viewer.add_static_point_light([0, 0.25, 0], light_option)

viewer.run()
viewer.cleanup()