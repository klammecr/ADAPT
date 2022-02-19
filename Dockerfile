FROM cyberbotics/webots:latest as base
LABEL org.opencontainers.image.authors="christopher.klammer@gmail.com"

# Grab the repos/package tools that we need for installations
RUN \
apt update \
&& apt install -y software-properties-common \
&& add-apt-repository universe \
&& apt update \
&& apt install -y curl gnupg lsb-release \
# Add the GPG key and authorize it with apt
&& curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
&& echo "deb [arch=amd64 signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu focal main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
# && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(source /etc/os-release && echo $UBUNTU_CODENAME) main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Third party - Install ROS2 and its dependencies
RUN \
apt update && apt install -y \
build-essential \
cmake \
git \
python3-colcon-common-extensions \
python3-flake8 \
python3-pip \
python3-pytest-cov \
python3-rosdep \
python3-setuptools \
python3-vcstool \
wget \
# install some pip packages needed for testing
&& python3 -m pip install -U \
flake8-blind-except \
flake8-builtins \
flake8-class-newline \
flake8-comprehensions \
flake8-deprecated \
flake8-docstrings \
flake8-import-order \
flake8-quotes \
pytest-repeat \
pytest-rerunfailures \
pytest \
setuptools \
&& python3 -m pip install -U importlib-metadata importlib-resources \
&& mkdir -p ~/ros2_galactic/src \
&& cd ~/ros2_galactic \
&& wget https://raw.githubusercontent.com/ros2/ros2/galactic/ros2.repos \
&& vcs import src < ros2.repos \
&& rosdep init \
&& rosdep update \
&& rosdep install --from-paths src --ignore-src -y --skip-keys "fastcdr rti-connext-dds-5.3.1 urdfdom_headers"