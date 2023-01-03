FROM ubuntu:20.04
LABEL maintainer="James Goppert <james.goppert@gmail.com>"

# Set default shell during Docker image build to bash
SHELL ["/bin/bash", "-c"]

COPY docker_clean.sh /docker_clean.sh
RUN chmod +x /docker_clean.sh

# Install base packages
RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get install --no-install-recommends -y \
		sudo \
		locales \
		&& \
	/docker_clean.sh

# set locale
RUN locale-gen en_US.UTF-8

# set user as default so install scripts look the same for local host install
RUN groupadd -r -g 110 render \
 && adduser --disabled-password --gecos '' user \
 && adduser user sudo \
 && adduser user render \
 && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER user

# initialise system locale
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8
# required to allow nanopb to build on ubuntu 22.04 currently
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV XDG_RUNTIME_DIR=/tmp/runtime-docker

# install dependencies using scripts in a manner that will cache build
# when one script is modified
COPY install/base.sh /tmp/install/base.sh
RUN /tmp/install/base.sh && /docker_clean.sh

COPY install/gazebo.sh /tmp/install/gazebo.sh
RUN /tmp/install/gazebo.sh && /docker_clean.sh

COPY install/ros.sh /tmp/install/ros.sh
RUN /tmp/install/ros.sh && /docker_clean.sh

COPY install/extra.sh /tmp/install/extra.sh
RUN /tmp/install/extra.sh && /docker_clean.sh

# enable apt auto-completion by deleting autoclean task
RUN sudo rm /etc/apt/apt.conf.d/docker-clean

# create setting directory for ignition gazebo
RUN mkdir -p /home/user/.ignition \
  && chown -R user:user /home/user/.ignition

# avoid .bashrc warning
RUN mkdir -p /home/user/.bash_completion.d

# create XDG runtime dir
RUN mkdir /tmp/runtime-docker && sudo chmod 700 /tmp/runtime-docker

# px4 simulation gazebo
RUN . /opt/ros/foxy/setup.sh \
  && git clone https://github.com/jgoppert/px4-simulation-ignition.git --depth 1 -b gazebo6 /tmp/px4-simulation-ignition \
  && cd /tmp/px4-simulation-ignition \
  && mkdir build && cd build \
  && cmake .. && make && cpack -G DEB \
  && sudo dpkg -i *.deb

# create workdir
RUN sudo mkdir -p /workdir && sudo chown -R user:user /workdir
WORKDIR /workdir

# setup .bashrc
RUN echo "source /workdir/install/setup.bash" >> ~/.bashrc

RUN colcon build --symlink-install --event-handlers console_direct+

# prevent terminator stderrr messages
ENV NO_AT_BRIDGE=1

CMD ["bash"]

# vim: set et fenc=utf-8 ff=unix ft=dockerfile sts=0 sw=2 ts=2 :
