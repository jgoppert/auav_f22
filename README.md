# IEEE Fall 2022 Autonomous UAV (AUAV) Competition Containers

## Submission
To write your solutions, fork this repository.

This repository consists of 4 docker containers and several source directories.
* auav_f22_sim: Simulation with ignition Gazebo Fortress.
* auav_f22_gcs: QGroundControl: Runs ground station.
* auav_f22_px4: PX4 Autopilot: This should match the Firmware on your drone (v1.12.3) do not change.
* auav_f22_onboard: Onboard computer running ROS, add your code here. It should directly deploy to the real drone. Try to keep the image small, it must be < 20G.

The source directories: sim/ws/src, onboard/ws/src are mounted inside the docker images. This allows for
rapid development. We recommend that you do all git version control commands on your host machine.

## Hardware Requirements
* Ubuntu 22.04 host computer
* NVidia graphics card

This repository uses docker and docker compose:
* https://docs.docker.com/desktop/install/ubuntu/

Docker now natively supports NVidia GPUs. We have tested docker with the following drivers:
```bash
sudo apt install nvidia-driver-515 libnvidia-gl-515-server
```

## Docker Images
This repository consists of 4 docker containers and several source directories.
* auav_f22_sim: Simulation with ignition Gazebo Fortress.
* auav_f22_gcs: QGroundControl: Runs ground station.
* auav_f22_px4: PX4 Autopilot: This should match the Firmware on your drone (v1.12.3) do not change.
* auav_f22_onboard: Onboard computer running ROS, made modifications here.

## Clone git submodules
```bash
git submodule update --init
```

## Pull
```bash
docker compose pull
```

## Run
```bash
docker compose up
```

## Build
If you need to rebuild the docker images, you can run:
```bash
docker compose build
```

## Connect to Running Container

```bash
docker compose exec onboard bash
```
