FROM ros:foxy-ros-base
LABEL maintainer="James Goppert <james.goppert@gmail.com>"

#  install dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  wget \
  unzip \
 	openjdk-8-jdk \
  vim \
  python3-pip \
  terminator \
  bash-completion \
  libcanberra-gtk3-module \
  ros-foxy-realsense2-camera \
  && apt-get -y autoremove \
	&& apt-get clean

# openvino install
RUN pip3 install openvino-dev[pytorch]==2021.4.2 pyros-genmsg

# setup user
RUN adduser --disabled-password --gecos '' docker \
 && adduser docker sudo \
 && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER docker

# Gradle (Required to build Fast-RTPS-Gen)
RUN wget -q "https://services.gradle.org/distributions/gradle-6.3-rc-4-bin.zip" -O /tmp/gradle-6.3-rc-4-bin.zip \
	&& sudo mkdir /opt/gradle \
	&& cd /tmp \
	&& sudo unzip -d /opt/gradle gradle-6.3-rc-4-bin.zip \
	&& sudo rm -rf /tmp/*

ENV PATH "/opt/gradle/gradle-6.3-rc-4/bin:$PATH"

# Fast-RTPS-Gen 1.0.4
RUN git clone --recursive https://github.com/eProsima/Fast-DDS-Gen.git -b v1.0.4 /tmp/Fast-RTPS-Gen-1.0.4 \
	&& cd /tmp/Fast-RTPS-Gen-1.0.4 \
	&& gradle assemble \
	&& sudo /opt/gradle/gradle-6.3-rc-4/bin/gradle install \
	&& sudo rm -rf /tmp/*

# px4_msgs
# https://docs.px4.io/v1.12/en/ros/ros2_comm.html
# lock down at v1.12.3 compat px4_msgs (8/16/21)
RUN . /opt/ros/foxy/setup.sh \
 && mkdir -p ~/px4_ros_com_ros2/src \
 && git clone https://github.com/PX4/px4_msgs.git ~/px4_ros_com_ros2/src/px4_msgs \
 && cd ~/px4_ros_com_ros2/src/px4_msgs \
 && git checkout e52b831 \
 && cd ~/px4_ros_com_ros2 \
 && colcon build --symlink-install --event-handlers console_direct+

# px4_ros_com
# lock down at v1.12.3 compat px4_ros_com (3/22/22)
RUN . ~/px4_ros_com_ros2/install/setup.sh \
 && git clone https://github.com/PX4/px4_ros_com.git ~/px4_ros_com_ros2/src/px4_ros_com \
 && cd ~/px4_ros_com_ros2/src/px4_ros_com \
 && git checkout 41f93ae \
 && cd ~/px4_ros_com_ros2 \
 && colcon build --symlink-install --event-handlers console_direct+

# setup .bashrc
RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc \
 && echo "source /home/docker/px4_ros_com_ros2/install/setup.bash" >> ~/.bashrc \
 && echo "source /home/docker/ws/install/setup.bash" >> ~/.bashrc

# ws
RUN . ~/.bashrc \
 && mkdir -p /home/docker/ws \
 && cd /home/docker/ws \
 && colcon build --symlink-install --event-handlers console_direct+

RUN mkdir -p /tmp/runtime-docker && chmod 700 /tmp/runtime-docker
ENV XDG_RUNTIME_DIR=/tmp/runtime-docker

# prevent terminator stderrr messages
ENV NO_AT_BRIDGE=1
WORKDIR /home/docker/ws
ENV ROS2_WS /home/docker/ws

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

# vim: set et fenc=utf-8 ff=unix ft=dockerfile sts=0 sw=2 ts=2 :
