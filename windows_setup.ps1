# Download and unzip Eigen because Eigen does ont have an official github repo
# that we can add as a submodule.
# Tls12 is needed to successfully download Eigen.
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
wget https://gitlab.com/libeigen/eigen/-/archive/3.3.8/eigen-3.3.8.zip -OutFile Eigen.3.3.8.zip
Expand-Archive Eigen.3.3.8.zip -DestinationPath externals
# Rename the folder.
mv externals/eigen-3.3.8 externals/eigen
rm Eigen.3.3.8.zip

# Download and unzip GLEW because building from the source is a huge pain, as
# suggested in their website.
# Tls12 is needed to successfully download glew.
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
wget https://github.com/nigels-com/glew/releases/download/glew-2.0.0/glew-2.0.0.zip -OutFile glew.2.0.0.zip
Expand-Archive glew.2.0.0.zip -DestinationPath externals
# Rename the folder.
mv externals/glew-2.0.0 externals/glew
rm glew.2.0.0.zip
