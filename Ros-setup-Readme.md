# ROS Humble Development Container

Simple Docker setup for ROS Humble development.

## Quick Start

```bash
# Build and start
docker compose build
docker compose up -d

# Connect
docker compose exec ros-humble bash

# Test ROS
ros2 --version
colcon --version
```

## Install New Packages

During development, if you need new packages:

1. Install in container:
```bash
sudo apt install ros-humble-gazebo-ros-pkgs
```

2. Add to `Dockerfile`:
```dockerfile
ros-humble-gazebo-ros-pkgs \
```

3. Rebuild:
```bash
docker compose build
docker compose up -d
```

## Storage

- **Host:** `./ros-packages/` → Container: `/home/cobot_ws/src`
- Packages built in container persist in volumes

## Development Flow

1. Edit code in `ros-packages/`
2. Build in container: `colcon build`
3. Test: `colcon test`
4. Commit to git: `git add ros-packages/ && git commit`

Done! ✅