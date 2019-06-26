# cython: language_level=3
# distutils: language = c++

import sys
import numpy as np

from libcpp.vector cimport vector
from libcpp.string cimport string
from libcpp cimport bool

# Option.
cdef extern from "../projects/opengl_viewer/include/option.h" namespace "opengl_viewer":
  cdef cppclass Option:
    Option() except +
    void SetIntOption(string& name, int value)
    void ClearIntOption(string& name)
    void ClearIntOption()
    bool HasIntOption(string& name)
    int GetIntOption(string& name)

    void SetFloatOption(string& name, float value)
    void ClearFloatOption(string& name)
    void ClearFloatOption()
    bool HasFloatOption(string& name)
    float GetFloatOption(string& name)

    void SetBoolOption(string& name, bool value)
    void ClearBoolOption(string& name)
    void ClearBoolOption()
    bool HasBoolOption(string& name)
    bool GetBoolOption(string& name)

    void SetStringOption(string& name, string& value)
    void ClearStringOption(string& name)
    void ClearStringOption()
    bool HasStringOption(string& name)
    string GetStringOption(string& name)

    void SetVectorOption(string& name, vector[float]& value)
    void ClearVectorOption(string& name)
    void ClearVectorOption()
    bool HasVectorOption(string& name)
    vector[float] GetVectorOptionPyBinding(string& name)

    void SetMatrixOption(string& name, vector[vector[float]]& value)
    void ClearMatrixOption(string& name)
    void ClearMatrixOption()
    bool HasMatrixOption(string& name)
    vector[vector[float]] GetMatrixOptionPyBinding(string& name)

cdef class PyglOption:
  cdef Option instance
  def __cinit__(self):
    self.instance = Option()

  def to_string(self, name):
    return bytes(name.encode('UTF-8'))

  def __setitem__(self, name, value):
    # Global options.
    if name in ['height', 'shadow sampling number', 'width',
                'texture row num', 'texture col num']:
      self.set_int_option(name, int(value))
    elif name in ['camera aspect ratio', 'camera field of view', 'camera pan speed',
                  'camera range max', 'camera range min', 'camera rotate speed',
                  'camera zoom speed', 'shadow acne bias', 'shadow sampling angle',
                  'shininess']:
      self.set_float_option(name, float(value))
    elif name in ['shadow']:
      self.set_bool_option(name, value)
    elif name in ['window name', 'texture mag filter']:
      self.set_string_option(name, str(value))
    elif name in ['background color', 'camera look at', 'camera pos', 'camera up']:
      self.set_vector_option(name, np.array(value, dtype=np.float32))
    # Local options.
    elif name in ['ambient', 'diffuse', 'specular']:
      self.set_vector_option(name, np.array(value, dtype=np.float32))
    elif name in ['model matrix', 'texture', 'uv']:
      self.set_matrix_option(name, np.array(value, dtype=np.float32))
    else:
      print('Unsupported name:', name)
      exit(0)

  def __getitem__(self, name):
    # Global options.
    if name in ['height', 'shadow sampling number', 'width',
                'texture row num', 'texture col num']:
      return int(self.get_int_option(name))
    elif name in ['camera aspect ratio', 'camera field of view', 'camera pan speed',
                  'camera range max', 'camera range min', 'camera rotate speed',
                  'camera zoom speed', 'shadow acne bias', 'shadow sampling angle',
                  'shininess']:
      return float(self.get_float_option(name))
    elif name in ['shadow']:
      return self.get_bool_option(name)
    elif name in ['window name', 'texture mag filter']:
      return str(self.get_string_option(name))
    elif name in ['background color', 'camera look at', 'camera pos', 'camera up']:
      return np.array(self.get_vector_option(name), dtype=np.float32)
    # Local options.
    elif name in ['ambient', 'diffuse', 'specular']:
      return np.array(self.get_vector_option(name), dtype=np.float32)
    elif name in ['model matrix', 'texture', 'uv']:
      return np.array(self.get_matrix_option(name), dtype=np.float32)
    else:
      print('Unsupported name:', name)
      exit(0)

  def set_int_option(self, name, value):
    self.instance.SetIntOption(self.to_string(name), value)

  def clear_int_option(self, name):
    self.instance.ClearIntOption(self.to_string(name))

  def clear_int_option(self):
    self.instance.ClearIntOption()

  def has_int_option(self, name):
    self.instance.HasIntOption(self.to_string(name))

  def get_int_option(self, name):
    return self.instance.GetIntOption(self.to_string(name))

  def set_float_option(self, name, value):
    self.instance.SetFloatOption(self.to_string(name), value)

  def clear_float_option(self, name):
    self.instance.ClearFloatOption(self.to_string(name))

  def clear_float_option(self):
    self.instance.ClearFloatOption()

  def has_float_option(self, name):
    self.instance.HasFloatOption(self.to_string(name))

  def get_float_option(self, name):
    return self.instance.GetFloatOption(self.to_string(name))

  def set_bool_option(self, name, value):
    self.instance.SetBoolOption(self.to_string(name), value)

  def clear_bool_option(self, name):
    self.instance.ClearBoolOption(self.to_string(name))

  def clear_bool_option(self):
    self.instance.ClearBoolOption()

  def has_bool_option(self, name):
    self.instance.HasBoolOption(self.to_string(name))

  def get_bool_option(self, name):
    return self.instance.GetBoolOption(self.to_string(name))

  def set_string_option(self, name, value):
    self.instance.SetStringOption(self.to_string(name), self.to_string(value))

  def clear_string_option(self, name):
    self.instance.ClearStringOption(self.to_string(name))

  def clear_string_option(self):
    self.instance.ClearStringOption()

  def has_string_option(self, name):
    self.instance.HasStringOption(self.to_string(name))

  def get_string_option(self, name):
    return self.instance.GetStringOption(self.to_string(name))

  def set_vector_option(self, name, value):
    self.instance.SetVectorOption(self.to_string(name), value.tolist())

  def clear_vector_option(self, name):
    self.instance.ClearVectorOption(self.to_string(name))

  def clear_vector_option(self):
    self.instance.ClearVectorOption()

  def has_vector_option(self, name):
    self.instance.HasVectorOption(self.to_string(name))

  def get_vector_option(self, name):
    return self.instance.GetVectorOptionPyBinding(self.to_string(name))

  def set_matrix_option(self, name, value):
    self.instance.SetMatrixOption(self.to_string(name), value.tolist())

  def clear_matrix_option(self, name):
    self.instance.ClearMatrixOption(self.to_string(name))

  def clear_matrix_option(self):
    self.instance.ClearMatrixOption()

  def has_matrix_option(self, name):
    self.instance.HasMatrixOption(self.to_string(name))

  def get_matrix_option(self, name):
    return self.instance.GetMatrixOptionPyBinding(self.to_string(name))

# SamplingAnimator.
cdef extern from "../projects/opengl_viewer/include/sampling_animator.h" namespace "opengl_viewer":
  cdef cppclass SamplingAnimator:
    SamplingAnimator(int sample_buffer) except +
    void AddSample(float t, vector[vector[float]]& transform)

cdef class PyglSamplingAnimator:
  cdef SamplingAnimator* instance
  def __cinit__(self, sample_buffer):
    self.instance = new SamplingAnimator(sample_buffer)

  def __dealloc__(self):
    del self.instance

  def add_sample(self, t, transform):
    transform = np.array(transform, dtype=np.float32).tolist()
    self.instance.AddSample(t, transform)

# Viewer.
cdef extern from "../projects/opengl_viewer/include/viewer.h" namespace "opengl_viewer":
  cdef cppclass Viewer:
    Viewer() except +
    void Initialize(Option& option)
    int AddStaticObject(vector[vector[float]]& vertex, vector[vector[int]]& face, Option& option)
    int AddDynamicObject(vector[vector[float]]& vertex, vector[vector[int]]& face,
                         SamplingAnimator* animator, Option& option)
    void AddStaticPointLight(vector[float]& position, Option& option)

    void RegisterLinearTimer(int fps)

    void Run()
    void Cleanup()

  cdef Viewer& GetViewer "opengl_viewer::Viewer::GetViewer"()

cdef class PyglViewer:
  cdef Viewer* instance
  def __cinit__(self, option):
    self.instance = &GetViewer()
    self.instance.Initialize((<PyglOption?>option).instance)

  def to_string(self, name):
    return bytes(name.encode('UTF-8'))

  def add_static_object(self, vertex, face, option):
    vertex = np.array(vertex, dtype=np.float32)
    face = np.array(face, dtype=np.int)
    return self.instance.AddStaticObject((vertex.T).tolist(), (face.T).tolist(), (<PyglOption?>option).instance)

  def add_dynamic_object(self, vertex, face, animator, option):
    vertex = np.array(vertex, dtype=np.float32)
    face = np.array(face, dtype=np.int)
    return self.instance.AddDynamicObject((vertex.T).tolist(), (face.T).tolist(),
                                          (<PyglSamplingAnimator?>animator).instance,
                                          (<PyglOption?>option).instance)

  def add_static_point_light(self, position, option):
    position = np.array(position, dtype=np.float32)
    self.instance.AddStaticPointLight(position.tolist(), (<PyglOption?>option).instance)

  def register_linear_timer(self, fps):
    self.instance.RegisterLinearTimer(fps)

  def run(self):
    self.instance.Run()

  def cleanup(self):
    self.instance.Cleanup()