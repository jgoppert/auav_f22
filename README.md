# IEEE Fall 2022 Autonomous UAV (AUAV) Competition Containers

* auav_f22_sim: Simulation with ignition gazebo fortress
* auav_f22_px4: PX4 Autopilot
* auav_f22_onboard: Onboard computer

## build
```bash
docker compose build
```
## run

```bash
docker compose up
```
## connect to running container

```bash
docker compose exec onboard bash
```

## troubleshooting

If window dragging is slow in ubuntu 22.04 on your host add

```bash
export __GL_SYNC_TO_VBLANK=0
```

To your /etc/environment.
