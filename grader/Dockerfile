FROM osrf/ros:foxy-desktop
LABEL maintainer="James Goppert <james.goppert@gmail.com>"

# install other dependencies
RUN apt-get update && apt-get -y --quiet --no-install-recommends install \
  vim \
  cmake \
  build-essential \
  git \
  && apt-get -y autoremove \
	&& apt-get clean

# setup user
RUN groupadd -r -g 110 render \
 && adduser --disabled-password --gecos '' docker \
 && adduser docker sudo \
 && adduser docker render \
 && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER docker
WORKDIR /home/docker/ws

RUN echo "source /opt/ros/foxy/setup.bash" >> ~/.bashrc \
  && echo "source /home/docker/ws/install/setup.bash" >> ~/.bashrc

RUN sudo colcon build --symlink-install --event-handlers console_direct+

RUN mkdir -p /tmp/runtime-docker && chmod 700 /tmp/runtime-docker
ENV XDG_RUNTIME_DIR=/tmp/runtime-docker

# prevent terminator stderrr messages
ENV NO_AT_BRIDGE=1

# prevent terminator stderrr messages
ENV NO_AT_BRIDGE=1
ENV ROS2_WS /home/docker/ws

ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

# vim: set et fenc=utf-8 ff=unix ft=dockerfile sts=0 sw=2 ts=2 :
