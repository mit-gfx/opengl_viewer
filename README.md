Author: Tao Du. PhD student at MIT CSAIL.

Email: taodu@csail.mit.edu

## Gallery
<img src="resources/pictures/monocopter.gif"/>

## Contents
* `externals/`
None of them are included by default. You need to use git submodule AND the
script I provided to download and configure them.
  * `eigen/`: downloaded by `{windows|linux|macos}_setup.sh`.
  * `glew/`: downloaded by `{windows|linux|macos}_setup.sh`.
  * `glfw/`: git submodule at 3.2.1.
  * `imgui/`: git submodule at v1.50.
  * `stb/`: git submodule at master.
* `projects/`
  * `opengl_viewer/`: a 3D viewer written in modern OpenGL (>= 3.3). Currently
    support point lights (static and dynamic), objects (static and dynamic),
    textures and soft shadows.
  * `test_opengl_viewer/`: provides two sample scenes to show the usage of this
    library:
    * `checkerboard/`: texture, moving lights and objects, soft shadows.
    * `point_light_shadow/`: only for testing the shadow map is correct.
* `resources/`:
  * `textures/`: images used in the sample scenes.
  * `meshes/`: sample object files.

## How to download:
Open your Git shell (Windows) / terminal (Linux and macOS) and type:
```bash
git clone --recursive https://github.com/mit-gfx/opengl_viewer.git
```
Navigate to the folder and run the bash script corresponding to your system:
```bash
cd opengl_viewer
```
For windows:
```bash
./windows_setup.ps1
```
For linux:
```bash
./linux_setup.sh
```
For macOS:
```bash
./macos_setup.sh
```

## How to build

### Windows (Windows 10 64bit + Visual Studio 2017)
* Open CMake and set this folder as the source folder.
* Out-of-source build is recommended.
* Click "Configure", then "Generate", then "Open Project".
* Press `F7` to build. Hopefully no errors will occur.
* Run `test_opengl_viewer` with proper input arguments (you can find them in
  `test_opengl_viewer.cpp`).

### Ubuntu (Ubuntu 16.04 64bit LTS + gcc 4.9.0)
* Make sure you have OpenGL and dependency libraries installed:
```bash
sudo apt-get install libgl1-mesa-dev mesa-common-dev xorg-dev
sudo apt-get install libglu1-mesa libglu1-mesa-dev
```
* Use CMake to do an out-of-source build:
```bash
(The root folder of this project): cd ../
mkdir opengl_viewer_build_gcc
cd opengl_viewer_build_gcc
cmake ../opengl_viewer
make
cd projects/test_opengl_viewer
./test_opengl_viewer checkerboard
```

### macOS (Sierra 10.12.3 + AppleClang 8.1.0)
Pretty much the same as Linux except that you don't need to install libraries:
```bash
cd ../
mkdir opengl_viewer_build_gcc
cd opengl_viewer_build_gcc
cmake ../opengl_viewer
make
cd projects/test_opengl_viewer
./test_opengl_viewer checkerboard
```

## How to use
There are two ways to integrate this library into your own project: you can
either build and compile the libraries, then manually include headers and link
libraries. Alternativaly, if you use CMake in your own project, you can add
this library as a subdirectory so that it can be integrated into your project
seamlessly. Below are the details of the two methods:

### Manually adding header and linking libraries
* Read "How to build" to generate `opengl_viewer.lib`. You should be able to
  find it in your build folder. Add this library in your project.

* Add the following include path in your project:
```bash
externals/eigen/
externals/glew/include/
externals/glfw/include/GLFW/
externals/imgui/
externals/stb/
projects/opengl_viewer/include/
```

* To use the library, simply include `opengl_viewer.h`. You can find sample
  code in the `test_opengl_viewer` project.

### Using CMake to integrate the library
Below we use `YOUR_PROJECT_ROOT` to refer to the root folder of your own
project. Normally it is also the folder where your top-level `CMakeLists.txt`
is.
* Use git clone, git submodule or simply copy and paste to put the whole
  library folder into your own project. Assume you want to put this library in
  a folder `YOUR_PROJECT_ROOT/externals/opengl_viewer`:
  * If you are using git:
    ```bash
    cd YOUR_PROJECT_ROOT
    mkdir externals
    cd externals
    git clone --recursive https://github/mit-gfx/opengl_viewer.git
    ```
  * If you use git submodule:
    ```bash
    cd YOUR_PROJECT_ROOT
    git submodule add https://github/mit-gfx/opengl_viewer.git
      externals/opengl_viewer
    ```
* In your root `CMakeLists.txt`, use the following command to add include
  directories:
  ```bash
  set(OPENGL_VIEWER_ROOT ${YOUR_PROJECT_ROOT}/externals/opengl_viewer)
  add_subdirectory(${OPENGL_VIEWER_ROOT})
  get_directory_property(OEPNGL_VIEWER_HEADER
    DIRECTORY ${OPENGL_VIEWER_ROOT}
    DEFINITION OPENGL_VIEWER_HEADER)
  ```
* In your own project, use the following command to add the include path:
  `include_directories(${OPENGL_VIEWER_HEADER})`

* Use the following command in your project to link the library:
  `target_link_libraries(your_project opengl_viewer)`

* We have provided a sample `CMakeLists.txt` in `projects/test_opengl_viewer/`
  for your reference.
