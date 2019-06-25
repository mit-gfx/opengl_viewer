from distutils.core import setup, Extension
from Cython.Build import cythonize

# Use python <this script name> build_ext --inplace
# to compile

setup(
  name = 'pygl_viewer',
  ext_modules = cythonize(
    Extension('pygl_viewer',
              sources=['viewer.pyx'],
              include_dirs=["../externals/eigen/",
                            "../externals/glew/include/",
                            "../externals/glfw/include/GLFW/",
                            "../externals/imgui/",
                            "../externals/stb/",
                            "../projects/opengl_viewer/include/"],
              language='c++',
              extra_objects=["../build/projects/opengl_viewer/libopengl_viewer.a",
                             "../build/externals/libimgui.a",
                             "../build/externals/libglew.a",
                             "../build/externals/glfw/src/libglfw3.a"],
              libraries=["GL", "glut", "X11", "Xi", "Xrandr", "Xxf86vm", "Xinerama", "Xcursor", "rt", "m", "pthread", "dl"],
              extra_compile_args=["-std=c++11"]),
  ),
)
