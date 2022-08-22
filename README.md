# IEEE Fall 2022 Autonomous UAV (AUAV) Competition Containers

* auav_f22_sim: Simulation with ignition Gazebo Fortress
* auav_f22_gcs: QGroundControl
* auav_f22_px4: PX4 Autopilot
* auav_f22_onboard: Onboard computer running ROS

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
