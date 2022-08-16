FROM ros:foxy-ros-base
LABEL maintainer="James Goppert <james.goppert@gmail.com>"

#  install dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  python3-pip \
  python3-bloom \
  fakeroot \
  dh-make \
  terminator \
  bash-completion \
  libcanberra-gtk3-module \
  ros-foxy-realsense2-camera \
  && apt-get -y autoremove \
	&& apt-get clean autoclean \
	&& rm -rf /var/lib/apt/lists/{apt,dpkg,cache,log} /tmp/* /var/tmp/*

# openvino install
RUN pip3 install openvino-dev[pytorch]==2021.4.2

# setup user
RUN adduser --disabled-password --gecos '' docker \
 && adduser docker sudo \
 && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker
WORKDIR /home/docker/ws

# Micro XRCE-DDS Agent (translates messages from autopilot into ROS2 DDS)
RUN git clone --recursive https://github.com/eProsima/Micro-XRCE-DDS-Agent.git -b v2.2.0 --depth 1 /tmp/dds \
  && cd /tmp/dds \
  && mkdir build && cd build \
  && cmake .. \
  && cmake --build . -j $(nproc) \
  && sudo make install \
  && sudo ldconfig \
  && rm -rf /tmp/*

# px4_msgs (defines PX4 messages for ROS2)
RUN . /opt/ros/foxy/setup.sh \
  && rosdep update \
  && mkdir -p /tmp/ws/src \
  && git clone --recursive --depth 1 https://github.com/PX4/px4_msgs.git /tmp/ws/src/px4_msgs \
  && ls /tmp/ws/src \
  && cd /tmp/ws/src/px4_msgs \
  && git checkout 7f89976 \
  && bloom-generate rosdebian \
  && DEB_BUILD_OPTIONS="nocheck parallel=$(nproc)" fakeroot debian/rules "binary --parallel" 1>/dev/null \
  && cd /tmp/ws/src && sudo dpkg -i *.deb \
  && rm -rf /tmp/*

RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc \
  && echo "source /home/docker/ws/install/setup.bash" >> ~/.bashrc

RUN colcon build --symlink-install

RUN mkdir -p /tmp/runtime-docker && chmod 700 /tmp/runtime-docker
ENV XDG_RUNTIME_DIR=/tmp/runtime-docker

# prevent terminator stderrr messages
ENV NO_AT_BRIDGE=1

# vim: set et fenc=utf-8 ff=unix ft=dockerfile sts=0 sw=2 ts=2 :
