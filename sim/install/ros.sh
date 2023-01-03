#!/bin/bash
set -e
ROS_VERSION="foxy"

sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt-get -y update
sudo apt-get -y upgrade
sudo DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y \
  build-essential \
  ros-${ROS_VERSION}-desktop \
  ros-${ROS_VERSION}-compressed-depth-image-transport \
  ros-${ROS_VERSION}-compressed-image-transport \
  ros-${ROS_VERSION}-image-transport-plugins \
  ros-${ROS_VERSION}-ros-ign-bridge \
  ros-${ROS_VERSION}-ros-ign-gazebo-demos \
  ros-${ROS_VERSION}-ros-ign-image \
  ros-${ROS_VERSION}-mavlink \
  libnvidia-gl-515-server \
  python3-rospkg \
  libcanberra-gtk3-module \
  python3-colcon-common-extensions

# setup .bashrc
echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc


