from distutils.core import setup, Extension
from Cython.Build import cythonize

# Use python <this script name> build_ext --inplace
# to compile

setup(
  name = 'pygl_option',
  ext_modules = cythonize(
    Extension('pygl_option',
              sources=['option.pyx'],
              include_dirs=["../projects/opengl_viewer/include/", "../externals/eigen/"],
              language='c++',
              #extra_objects=["build/common/libcommon.a"],
              extra_compile_args=["-std=c++11"]),
  ),
)
