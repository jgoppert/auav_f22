# IEEE Fall 2022 Autonomous UAV (AUAV) Competition Containers

* auav_f22_sim: Simulation with ignition gazebo fortress
* auav_f22_px4: PX4 Autopilot
* auav_f22_onboard: Onboard computer

## Clone git submodules
```bash
git submodule update --init
```

## Build
```bash
docker compose build
```

## Run
```bash
docker compose up
```

## Connect to Running Container

```bash
docker compose exec onboard bash
```
