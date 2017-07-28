#!/bin/sh

# Download and unzip Eigen because Eigen does ont have an official github repo
# that we can add as a submodule.
curl -LOk http://bitbucket.org/eigen/eigen/get/3.3.4.zip
unzip 3.3.4.zip -d externals
# Rename the folder.
mv externals/eigen-eigen-5a0156e40feb externals/eigen
rm 3.3.4.zip

# Download and unzip GLEW because building from the source is a huge pain, as
# suggested in their website.
curl -LOk https://github.com/nigels-com/glew/releases/download/glew-2.0.0/glew-2.0.0.zip
unzip glew-2.0.0.zip -d externals
# Rename the folder.
mv externals/glew-2.0.0 externals/glew
rm glew-2.0.0.zip
