#!/bin/sh

# Download and unzip Eigen because Eigen does ont have an official github repo
# that we can add as a submodule.
wget https://gitlab.com/libeigen/eigen/-/archive/3.3.4/eigen-3.3.4.zip --header "Referer: gitlab.com"


unzip eigen-3.3.4.zip -d externals
# Rename the folder.
mv externals/eigen-3.3.4 externals/eigen
rm eigen-3.3.4.zip

# Download and unzip GLEW because building from the source is a huge pain, as
# suggested in their website.
wget https://github.com/nigels-com/glew/releases/download/glew-2.0.0/glew-2.0.0.zip
unzip glew-2.0.0.zip -d externals
# Rename the folder.
mv externals/glew-2.0.0 externals/glew
rm glew-2.0.0.zip
